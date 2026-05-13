"""Lesson 12: real model loop with local tool execution.

The earlier lessons used fake_model so the agent mechanics were easy to see.
This lesson keeps the same local tool loop, but makes the model function
swappable:

- fake_model runs with no API key and keeps the lesson deterministic.
- real_model calls the OpenAI Responses API when USE_REAL_MODEL=1.

The important boundary is this: the model only decides what JSON to return.
Your Python code still parses that JSON, runs local tools, records observations,
handles failures, and stops after MAX_STEPS.
"""

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


MAX_STEPS = 4
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT / ".env"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.4-mini"


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


ModelFunction = Callable[[list[Message]], str]


def load_dotenv(path: Path = DOTENV_PATH) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()

        if not stripped_line or stripped_line.startswith("#"):
            continue

        if "=" not in stripped_line:
            continue

        key, value = stripped_line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")

        if key and key not in os.environ:
            os.environ[key] = value


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

    if latest_message.role == "tool":
        return make_message(f"Tool result:\n{latest_message.content}")

    if latest_message.role != "user":
        return make_message("I am waiting for a user request.")

    if "count words" in user_text:
        return make_tool_call("count_words", make_count_words_argument("real model loop"))

    if "uppercase" in user_text:
        return make_tool_call("uppercase_text", json.dumps({"text": "local tools still run locally"}))

    if "bad tool" in user_text:
        return make_tool_call("missing_tool", "{}")

    return make_message("I can answer directly without a tool.")


def build_model_prompt(transcript: list[Message]) -> str:
    transcript_text = "\n".join(
        f"{message.role.upper()}: {message.content}" for message in transcript
    )
    return (
        "You are the model inside a small teaching agent.\n"
        "Return exactly one JSON object and no Markdown.\n"
        "Allowed response shapes:\n"
        '{"type": "message", "role": "assistant", "content": "..."}\n'
        '{"type": "tool_call", "name": "count_words", "argument": "{\\"text\\": \\"...\\"}"}\n'
        '{"type": "tool_call", "name": "uppercase_text", "argument": "{\\"text\\": \\"...\\"}"}\n'
        "Use a tool only when it helps answer the latest user message.\n\n"
        f"Transcript:\n{transcript_text}"
    )


def extract_response_text(response_data: dict) -> str:
    if isinstance(response_data.get("output_text"), str):
        return response_data["output_text"]

    output_parts: list[str] = []
    for output_item in response_data.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") in {"output_text", "text"}:
                output_parts.append(content_item.get("text", ""))

    return "\n".join(part for part in output_parts if part).strip()


def real_model(transcript: list[Message]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return make_message("Set OPENAI_API_KEY before running with USE_REAL_MODEL=1.")

    request_body = {
        "model": os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        "input": build_model_prompt(transcript),
    }

    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        error_text = error.read().decode("utf-8", errors="replace")
        return make_message(f"OpenAI API error: {error.code}\n{error_text}")
    except urllib.error.URLError as error:
        return make_message(f"Network error: {error.reason}")

    response_text = extract_response_text(response_data)
    if not response_text:
        return make_message("OpenAI API returned no text output.")

    return response_text


def choose_model_function() -> ModelFunction:
    if os.environ.get("USE_REAL_MODEL") == "1":
        return real_model
    return fake_model


def parse_model_output(raw_output: str) -> Message | ToolCall:
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def count_words(argument: str) -> str:
    data = parse_tool_argument(argument, required_keys={"text"})
    text = data["text"]
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    return f"word_count={len(text.split())}"


def uppercase_text(argument: str) -> str:
    data = parse_tool_argument(argument, required_keys={"text"})
    text = data["text"]
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    return text.upper()


def parse_tool_argument(argument: str, required_keys: set[str]) -> dict:
    try:
        data = json.loads(argument)
    except json.JSONDecodeError as error:
        raise ValueError("argument must be JSON") from error

    if set(data) != required_keys:
        expected = ", ".join(sorted(required_keys))
        raise ValueError(f"expected exactly these keys: {expected}")

    return data


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
    model: ModelFunction,
    tools: dict[str, Callable[[str], str]],
) -> None:
    transcript.append(Message(role="user", content=user_prompt))

    for step_number in range(1, MAX_STEPS + 1):
        print(f"STEP {step_number}")
        raw_model_output = model(transcript)
        print("RAW MODEL OUTPUT:", raw_model_output)

        try:
            model_output = parse_model_output(raw_model_output)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            transcript.append(Message(role="assistant", content=f"ERROR: bad model output: {error}"))
            return

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
    load_dotenv()

    model = choose_model_function()
    tools = {
        "count_words": count_words,
        "uppercase_text": uppercase_text,
    }

    prompts = [
        "Count words",
        "Uppercase this text",
        "Use a bad tool",
    ]

    for prompt in prompts:
        print("=" * 60)
        print(f"USER: {prompt}")
        transcript: list[Message] = []
        run_agent_loop(transcript, prompt, model, tools)
        print()
        print_transcript(transcript)
        print()

    # TODO: Run once with the fake model and identify where local tool execution happens.
    # TODO: Set USE_REAL_MODEL=1 and OPENAI_API_KEY, then run the lesson with a real model.
    # TODO: Add one more local tool and teach both build_model_prompt and fake_model about it.


if __name__ == "__main__":
    main()
