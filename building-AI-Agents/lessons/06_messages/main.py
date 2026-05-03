"""Lesson 06: explicit messages.

Real agents do not pass around one loose string forever. They keep a transcript:
user messages, assistant messages, tool calls, and tool observations.

This lesson makes that structure visible without using an external model.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


def fake_model(transcript: list[Message]) -> Message | ToolCall:
    """Read the transcript and return the next assistant action."""
    latest_message = transcript[-1]

    if latest_message.role == "user" and "uppercase" in latest_message.content.lower():
        text = latest_message.content.lower().split("uppercase", 1)[1].strip()
        return ToolCall(name="uppercase", argument=text)

    if latest_message.role == "tool":
        return Message(role="assistant", content=f"The tool returned: {latest_message.content}")

    return Message(role="assistant", content="I can answer this without a tool.")


def uppercase(text: str) -> str:
    return text.upper()


def run_turn(user_prompt: str) -> list[Message]:
    transcript = [Message(role="user", content=user_prompt)]
    tools = {"uppercase": uppercase}

    model_output = fake_model(transcript)
    print("MODEL OUTPUT:", model_output)

    if isinstance(model_output, ToolCall):
        observation = tools[model_output.name](model_output.argument)
        transcript.append(Message(role="tool", content=observation))
        print("TOOL OBSERVATION:", observation)

        final_message = fake_model(transcript)
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

    # TODO: Add a second tool and a second user prompt.
    # TODO: Print how many messages are in the transcript.


if __name__ == "__main__":
    main()
