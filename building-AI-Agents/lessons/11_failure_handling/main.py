"""Lesson 11: failure handling in an agent loop.

Real agents do not only handle happy paths. A model can ask for a tool that
does not exist, pass bad arguments to a real tool, or keep asking for tools
without ever producing a final answer.

This lesson adds three guardrails:

1. Unknown tool calls become observations instead of crashes.
2. Bad tool arguments become observations instead of crashes.
3. The loop stops after MAX_STEPS tool calls.

This is still a fake model. The goal is to make the control flow obvious before
using a real model.
"""

import json
from dataclasses import dataclass
from typing import Callable


MAX_STEPS = 3


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


def make_count_words_argument(text: str) -> str:
    return json.dumps({"text": text})


def latest_user_text(transcript: list[Message]) -> str:
    for message in reversed(transcript):
        if message.role == "user":
            return message.content.lower()
    return ""


def fake_model(transcript: list[Message]) -> str:
    latest_message = transcript[-1]
    user_text = latest_user_text(transcript)

    if latest_message.role == "tool" and latest_message.content.startswith("ERROR:"):
        return make_message(f"I could not complete the request.\n{latest_message.content}")

    if latest_message.role == "tool" and "loop forever" in user_text:
        return make_tool_call("count_words", make_count_words_argument("again"))

    if latest_message.role == "tool":
        return make_message(f"Tool result:\n{latest_message.content}")

    if latest_message.role != "user":
        return make_message("I am waiting for a user request.")

    if "count words" in user_text:
        return make_tool_call("count_words", make_count_words_argument("agents use tools"))

    if "count numbers" in user_text:
        return make_tool_call("count_words", make_count_words_argument(123))

    if "missing tool" in user_text:
        return make_tool_call("read_file", "README.md")

    if "bad argument" in user_text:
        return make_tool_call("count_words", "not json")

    if "loop forever" in user_text:
        return make_tool_call("count_words", make_count_words_argument("start"))

    return make_message("I do not need a tool for that.")


def parse_model_output(raw_output: str) -> Message | ToolCall:
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def count_words(argument: str) -> str:
    try:
        data = json.loads(argument)
    except json.JSONDecodeError as error:
        raise ValueError("argument must be JSON") from error

    if set(data) != {"text"}:
        raise ValueError("expected exactly one key: text")

    if not isinstance(data["text"], str):
        raise ValueError("text must be a string")

    words = data["text"].split()
    return f"word_count={len(words)}"


def call_tool(tool_call: ToolCall, tools: dict[str, Callable[[str], str]]) -> str:
    if tool_call.name not in tools:
        available_tools = ", ".join(sorted(tools))
        return f"ERROR: unknown tool {tool_call.name!r}. Available tools: {available_tools}"

    try:
        return tools[tool_call.name](tool_call.argument)
    except ValueError as error:
        return f"ERROR: bad arguments for {tool_call.name!r}: {error}"


def run_agent_loop(
    transcript: list[Message],
    user_prompt: str,
    tools: dict[str, Callable[[str], str]],
) -> None:
    transcript.append(Message(role="user", content=user_prompt))

    for step_number in range(1, MAX_STEPS + 1):
        print(f"STEP {step_number}")
        raw_model_output = fake_model(transcript)
        print("RAW MODEL OUTPUT:", raw_model_output)

        model_output = parse_model_output(raw_model_output)
        print("PARSED MODEL OUTPUT:", model_output)

        if isinstance(model_output, Message):
            transcript.append(model_output)
            return

        observation = call_tool(model_output, tools)
        transcript.append(Message(role="tool", content=observation))
        print("TOOL OBSERVATION:", observation)

    transcript.append(
        Message(
            role="assistant",
            content=f"ERROR: stopped after {MAX_STEPS} tool calls without a final answer.",
        )
    )


def print_transcript(transcript: list[Message]) -> None:
    print("TRANSCRIPT:")
    for index, message in enumerate(transcript, start=1):
        print(f"{index}. {message.role.upper()}: {message.content}")


def main() -> None:
    tools = {"count_words": count_words}

    prompts = [
        "Count words",
        "Use a missing tool",
        "Use a bad argument",
        "Loop forever",
    ]
    
    prompts.append("count numbers")

    for prompt in prompts[4:]:
        print("=" * 60)
        print(f"USER: {prompt}")
        transcript: list[Message] = []
        run_agent_loop(transcript, prompt, tools)
        print()
        print_transcript(transcript)
        print()

    # TODO: Add a prompt that makes fake_model call count_words with {"text": 123}.
    # TODO: Handle that failure without crashing.
    # TODO: Lower MAX_STEPS to 2 and observe how the loop behavior changes.


if __name__ == "__main__":
    main()
