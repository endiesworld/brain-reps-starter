"""Lesson 12: real model loop with local tool execution.

This lesson uses only a real model call. There is no fake model and no fallback
model path.

The important boundary is this: the real model only decides what JSON to return.
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
DEFAULT_MODEL = "gpt-5-mini"
USE_MODEL = "gpt-5.5"

MAX_FILE_CHARS = 1200


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


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


def build_model_prompt(transcript: list[Message]) -> str:
    transcript_text = "\n".join(
        f"{message.role.upper()}: {message.content}" for message in transcript
    )
    return (
        "You are the real model inside a small teaching agent.\n"
        "Return exactly one JSON object and no Markdown.\n"
        "Allowed response shapes:\n"
        '{"type": "message", "role": "assistant", "content": "..."}\n'
        '{"type": "tool_call", "name": "count_words", "argument": "{\\"text\\": \\"...\\"}"}\n'
        '{"type": "tool_call", "name": "uppercase_text", "argument": "{\\"text\\": \\"...\\"}"}\n'
        '{"type": "tool_call", "name": "read_file", "argument": "{\\"path\\": \\"...\\"}"}\n'
        "When the latest user message asks you to count words, call count_words.\n"
        "When the latest user message asks you to uppercase text, call uppercase_text.\n"
        "When the latest user message asks you to summarize a file, call read_file.\n"
        "When the latest transcript message is a TOOL observation, answer with a final message.\n"
        "Use a direct message only when no tool is needed.\n\n"
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


def call_real_model(transcript: list[Message]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your shell or in the repo .env file.")

    request_body = {
        "model": USE_MODEL, # os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
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
        raise RuntimeError(f"OpenAI API error: {error.code}\n{error_text}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Network error: {error.reason}") from error

    response_text = extract_response_text(response_data)
    if not response_text:
        raise RuntimeError("OpenAI API returned no text output.")

    return response_text


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

def safe_project_path(path_text: str) -> Path | None:
    requested_path = (PROJECT_ROOT / path_text).resolve()
    
    print(f"Requested path: {requested_path}")

    if requested_path == PROJECT_ROOT:
        return None

    if PROJECT_ROOT not in requested_path.parents:
        return None

    return requested_path

def read_file(argument: str) -> str:
    data = parse_tool_argument(argument, required_keys={"path"})
    path = safe_project_path(data["path"])
    
    print(f"Safe path: {path}")
    if path is None:
        return f"Blocked path: {path}"

    if not path.exists():
        return f"File not found: {data['path']}"

    if not path.is_file():
        return f"Not a file: {data['path']}"

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return f"{data['path']} is empty."

    # if len(content) > MAX_FILE_CHARS:
    #     content = content[:MAX_FILE_CHARS].rstrip() + "\n... (truncated)"

    return f"{data['path']}:\n{content}"


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
    tools: dict[str, Callable[[str], str]],
) -> None:
    transcript.append(Message(role="user", content=user_prompt))

    for step_number in range(1, MAX_STEPS + 1):
        print(f"STEP {step_number}")
        raw_model_output = call_real_model(transcript)
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

    tools = {
        "count_words": count_words,
        "uppercase_text": uppercase_text,
        "read_file": read_file,
        
    }

    prompts = [
        "Count the words in exactly this text: real models call local tools",
        "Uppercase exactly this text: local tools still run locally",
        "Answer directly: what decides whether a tool runs in this program?",
    ]
    prompts.append("Summarize the contents of practice/python_engineering/ROADMAP.md")
    prompts.append("Write a brief summary on Agent Harness")
    for prompt in prompts[3:]:
        print("=" * 60)
        print(f"USER: {prompt}")
        transcript: list[Message] = []
        run_agent_loop(transcript, prompt, tools)
        print()
        print_transcript(transcript)
        print()

    # TODO: Change OPENAI_MODEL and observe whether the JSON decisions change.
    # TODO: Add one more local tool, then teach build_model_prompt when to call it.
    # TODO: Add a prompt that should not use a tool and confirm the model answers directly.


if __name__ == "__main__":
    main()
