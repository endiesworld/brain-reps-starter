"""Lesson 09: file-reading tool with path safety.

Coding agents need to inspect files before they can answer questions or edit
code. This lesson adds a file-reading tool that only reads files inside the
project directory.

This is still a fake model. The real behavior is in the agent loop: parse a
tool call, validate the requested path, read the file, and return the
observation to the transcript.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAX_FILE_CHARS = 1200


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


def make_message(content: str) -> str:
    return json.dumps({"type": "message", "role": "assistant", "content": content})


def make_tool_call(name: str, argument: str) -> str:
    return json.dumps({"type": "tool_call", "name": name, "argument": argument})


def extract_path(text: str, marker: str) -> str:
    marker_start = text.lower().find(marker)
    if marker_start == -1:
        return ""
    path_start = marker_start + len(marker)
    return text[path_start:].strip().strip("'\"")


def fake_model(transcript: list[Message]) -> str:
    latest_message = transcript[-1]
    latest_text = latest_message.content.lower()

    if latest_message.role == "tool":
        return make_message(f"File result:\n{latest_message.content}")

    if latest_message.role != "user":
        return make_message("I am waiting for a user request.")

    if "read file" in latest_text:
        path_text = extract_path(latest_message.content, "read file")
        return make_tool_call("read_file", path_text)

    if "read the readme" in latest_text:
        return make_tool_call("read_file", "README.md")

    if "read project memory" in latest_text:
        return make_tool_call("read_file", "PROJECT_MEMORY.md")

    if "read the roadmap" in latest_text:
        return make_tool_call("read_file", "ROADMAP.md")
    
    if "read this" in latest_text:
        path_text = extract_path(latest_message.content, "read this")
        return make_tool_call("read_file", path_text)

    if "read outside" in latest_text:
        return make_tool_call("read_file", "../README.md")

    return make_message("I do not need to read a file for that.")


def parse_model_output(raw_output: str) -> Message | ToolCall:
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def safe_project_path(path_text: str) -> Path | None:
    requested_path = (PROJECT_ROOT / path_text).resolve()

    if requested_path == PROJECT_ROOT:
        return None

    if PROJECT_ROOT not in requested_path.parents:
        return None

    return requested_path


def read_file(path_text: str) -> str:
    path = safe_project_path(path_text)
    if path is None:
        return f"Blocked path: {path_text}"

    if not path.exists():
        return f"File not found: {path_text}"

    if not path.is_file():
        return f"Not a file: {path_text}"

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return f"{path_text} is empty."

    if len(content) > MAX_FILE_CHARS:
        content = content[:MAX_FILE_CHARS].rstrip() + "\n... (truncated)"

    return f"{path_text}:\n{content}"


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
    tools = {"read_file": read_file}

    prompts = [
        "Read the README",
        "Read project memory",
        "Read file lessons/01_prompt_response/main.py",
        "Read outside the project",
    ]

    # for prompt in prompts:
    #     print(f"\nUSER: {prompt}")
    #     run_turn(transcript, prompt, tools)

    # print()
    # print_transcript(transcript)

    # TODO: Add a prompt that reads ROADMAP.md.
    prompts.append("read the roadmap")
    # TODO: Teach fake_model how to request that file.
    # TODO: Add one more blocked path example.
    prompts.append("read this /home/endy/Documents/Projects/brain-reps-starter/README.md")

    for prompt in prompts[4:]:
        print(f"\nUSER: {prompt}")
        run_turn(transcript, prompt, tools)


if __name__ == "__main__":
    main()
