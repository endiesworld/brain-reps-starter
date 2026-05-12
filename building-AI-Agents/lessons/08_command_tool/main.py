"""Lesson 08: command tool with an allowlist.

Coding agents need to inspect projects and run checks, but they should not get
arbitrary shell access. This lesson adds a command-running tool that only runs
commands approved by the runtime.
"""

import json
import shlex
import subprocess
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


ALLOWED_COMMANDS = {
    ("pwd",),
    ("ls",),
    ("python3", "--version"),
    ("python3", "lessons/01_prompt_response/main.py"),
    ("which", "node"),
    ("hostnamectl", "status"),
}


def make_message(content: str) -> str:
    return json.dumps({"type": "message", "role": "assistant", "content": content})


def make_tool_call(name: str, argument: str) -> str:
    return json.dumps({"type": "tool_call", "name": name, "argument": argument})


def fake_model(transcript: list[Message]) -> str:
    latest_message = transcript[-1]
    latest_text = latest_message.content.lower()

    if latest_message.role == "tool":
        return make_message(f"Command result:\n{latest_message.content}")

    if latest_message.role != "user":
        return make_message("I am waiting for a user request.")

    if "current directory" in latest_text:
        return make_tool_call("run_command", "pwd")

    if "list files" in latest_text:
        return make_tool_call("run_command", "ls")

    if "python version" in latest_text:
        return make_tool_call("run_command", "python3 --version")

    if "run lesson 1" in latest_text:
        return make_tool_call("run_command", "python3 lessons/01_prompt_response/main.py")

    if "delete files" in latest_text:
        return make_tool_call("run_command", "rm -rf lessons")
    
    if "node" in latest_text:
        return make_tool_call("run_command", "which node")
    
    if "os info" in latest_text or "system info" in latest_text or "hostname" in latest_text:
        return make_tool_call("run_command", "hostnamectl status")
    
    if "request new command" in latest_text:
        return make_message("I would like to run 'df -h' to check disk usage.")

    return make_message("I do not need a command for that.")


def parse_model_output(raw_output: str) -> Message | ToolCall:
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def run_command(command_text: str) -> str:
    command = tuple(shlex.split(command_text))

    if command not in ALLOWED_COMMANDS:
        return f"Blocked command: {command_text}"

    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    output = completed.stdout.strip() or completed.stderr.strip()
    if not output:
        output = "(no output)"

    return f"exit_code={completed.returncode}\n{output}"


def run_turn(
    transcript: list[Message],
    user_prompt: str,
    tools: dict[str, Callable[[str], str]],
) -> None:
    transcript.append(Message(role="user", content=user_prompt))

    raw_model_output = fake_model(transcript)
    print("RAW MODEL OUTPUT:", raw_model_output)
    model_output = parse_model_output(raw_model_output)
    print("PARSED MODEL OUTPUT:", model_output)

    if isinstance(model_output, Message):
        transcript.append(model_output)
        return

    if model_output.name not in tools:
        transcript.append(Message(role="assistant", content=f"Error: unknown tool {model_output.name!r}"))
        return

    observation = tools[model_output.name](model_output.argument)
    transcript.append(Message(role="tool", content=observation))
    print("TOOL OBSERVATION:", observation)

    raw_final_output = fake_model(transcript)
    print("RAW MODEL OUTPUT:", raw_final_output)
    final_output = parse_model_output(raw_final_output)
    if isinstance(final_output, ToolCall):
        raise RuntimeError("This lesson expects one tool call per turn.")
    transcript.append(final_output)


def print_transcript(transcript: list[Message]) -> None:
    print("TRANSCRIPT:")
    for index, message in enumerate(transcript, start=1):
        print(f"{index}. {message.role.upper()}: {message.content}")


def main() -> None:
    transcript: list[Message] = []
    tools = {"run_command": run_command}

    prompts = [
        "What is the current directory?",
        "List files",
        "What Python version is installed?",
        "Run lesson 1",
        "Delete files",
    ]

    for prompt in prompts:
        print(f"\nUSER: {prompt}")
        run_turn(transcript, prompt, tools)

    print()
    print_transcript(transcript)

    # TODO: Add one more safe command to ALLOWED_COMMANDS.
    print("==============================")
    prompt = "which node is installed?"
    print(f"\nUSER: {prompt}")
    run_turn(transcript, prompt, tools)
    print()
    
    print("==============================")
    prompt = "Give me system info"
    print(f"\nUSER: {prompt}")
    run_turn(transcript, prompt, tools)
    print()    
    
    # TODO: Add a prompt that asks the model to request your new command.
    print("==============================")
    prompt = "Request new command to check disk usage"
    print(f"\nUSER: {prompt}")
    run_turn(transcript, prompt, tools)
    print()
    print_transcript(transcript)


if __name__ == "__main__":
    main()
