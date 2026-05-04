"""Lesson 06: explicit messages.

Real agents do not pass around one loose string forever. They keep a transcript:
user messages, assistant messages, tool calls, and tool observations.

Models return text. Your program parses that text into structured objects it can
act on.

This lesson makes that structure visible without using an external model.
"""

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


def fake_model(transcript: list[Message]) -> str:
    """Read the transcript and return raw JSON text like a model response."""
    latest_message = transcript[-1]

    if latest_message.role == "user" and "uppercase" in latest_message.content.lower():
        text = latest_message.content.lower().split("uppercase", 1)[1].strip()
        return json.dumps({"type": "tool_call", "name": "uppercase", "argument": text})
    
    elif latest_message.role == "user" and "calculate" in latest_message.content.lower():
        text = latest_message.content.lower().split("calculate", 1)[1].strip()
        return json.dumps({"type": "tool_call", "name": "calculator", "argument": text}) 

    if latest_message.role == "tool":
        return json.dumps(
            {
                "type": "message",
                "role": "assistant",
                "content": f"The tool returned: {latest_message.content}",
            }
        )

    return json.dumps(
        {
            "type": "message",
            "role": "assistant",
            "content": "I can answer this without a tool.",
        }
    )


def parse_model_output(raw_output: str) -> Message | ToolCall:
    """Convert raw model text into objects the program knows how to handle."""
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def uppercase(text: str) -> str:
    return text.upper()

def calculator(expr: str) -> str :
    allowed = set("0123456789+-*/(). ")
    expr = expr.strip()
    not_allowed = [char for char in expr if char not in allowed ]
    if not_allowed :
        return "Error: unsupported expression"
    return str(eval(expr, {"__builtins__": {}}, {}))

def run_turn(user_prompt: str) -> list[Message]:
    transcript = [Message(role="user", content=user_prompt)]
    tools = {"uppercase": uppercase, "calculator": calculator}

    raw_model_output = fake_model(transcript)
    print("RAW MODEL OUTPUT:", raw_model_output)
    model_output = parse_model_output(raw_model_output)
    print("PARSED MODEL OUTPUT:", model_output)

    if isinstance(model_output, ToolCall):
        observation = tools[model_output.name](model_output.argument)
        transcript.append(Message(role="tool", content=observation))
        print("TOOL OBSERVATION:", observation)

        raw_final_output = fake_model(transcript)
        print("RAW MODEL OUTPUT:", raw_final_output)
        final_message = parse_model_output(raw_final_output)
        if isinstance(final_message, ToolCall):
            raise RuntimeError("This lesson expects only one tool call.")
        transcript.append(final_message)
    else:
        transcript.append(model_output)

    return transcript


def main() -> None:
    transcript = run_turn("Uppercase agent transcript")

    print("TRANSCRIPT:")
    for message in transcript:
        print(f"{message.role.upper()}: {message.content}")

    print("========== RESULTS OF SECOND PROMPT ==========")
    # TODO: Add a second tool and a second user prompt.
    transcript = run_turn("calculate 50 * 75")
    # TODO: Print how many messages are in the transcript.
    print(f"Number of messages in transcript: {len(transcript)}")
    print("TRANSCRIPT:")
    for message in transcript:
        print(f"{message.role.upper()}: {message.content}")


if __name__ == "__main__":
    main()
