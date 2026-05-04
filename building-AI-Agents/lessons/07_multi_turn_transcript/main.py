"""Lesson 07: multi-turn transcripts.

Lesson 06 showed one turn. This lesson keeps one transcript across multiple
turns so the model can use earlier messages before deciding what to do next.
"""

import json
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


def make_message(content: str) -> str:
    return json.dumps({"type": "message", "role": "assistant", "content": content})


def make_tool_call(name: str, argument: str) -> str:
    return json.dumps({"type": "tool_call", "name": name, "argument": argument})


def last_tool_message(transcript: list[Message]) -> Message | None:
    for message in reversed(transcript):
        if message.role == "tool":
            return message
    return None


def fake_model(transcript: list[Message]) -> str:
    """Return raw JSON text based on the full transcript."""
    latest_message = transcript[-1]
    latest_text = latest_message.content.lower()

    if latest_message.role == "tool":
        return make_message(f"The tool returned: {latest_message.content}")

    if latest_message.role != "user":
        return make_message("I am waiting for the next user message.")

    if "uppercase" in latest_text:
        text = latest_message.content.split("uppercase", 1)[1].strip()
        return make_tool_call("uppercase", text)

    if "calculate" in latest_text:
        expression = latest_message.content.split("calculate", 1)[1].strip()
        return make_tool_call("calculator", expression)

    if "last tool" in latest_text:
        tool_message = last_tool_message(transcript)
        if tool_message is None:
            return make_message("No tool has been used yet.")
        return make_message(f"The last tool result was: {tool_message.content}") 
    
    if "how many tool results" in latest_text:
        count = sum(1 for message in transcript if message.role == "tool")
        return make_message(f"There are {count} tool results in the transcript.")

    return make_message("I can answer this without a tool.")


def parse_model_output(raw_output: str) -> Message | ToolCall:
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def uppercase(text: str) -> str:
    return text.upper()


def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    expression = expression.strip()
    if any(char not in allowed for char in expression):
        return "Error: unsupported expression"
    return str(eval(expression, {"__builtins__": {}}, {}))


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
    tools = {"uppercase": uppercase, "calculator": calculator}

    prompts = [
        "uppercase agent transcript",
        "calculate 50 * 75",
        "What was the last tool result?",
    ]

    for prompt in prompts:
        print(f"\nUSER: {prompt}")
        run_turn(transcript, prompt, tools)

    print()
    print_transcript(transcript)
    print("MESSAGE COUNT:", len(transcript))

    # TODO: Add a fourth prompt that does not need a tool.
    fourth_prompt = "What is 2 + 2?"
    print(f"\nUSER: {fourth_prompt}")
    run_turn(transcript, fourth_prompt, tools)
    print()
    print_transcript(transcript)
    print("MESSAGE COUNT:", len(transcript))
    
    # TODO: Teach fake_model to answer "How many tool results are in the transcript?"
    fift_prompt = "How many tool results are in the transcript?"
    print(f"\nUSER: {fift_prompt}")
    run_turn(transcript, fift_prompt, tools)
    print()
    print_transcript(transcript)
    print("MESSAGE COUNT:", len(transcript))


if __name__ == "__main__":
    main()
