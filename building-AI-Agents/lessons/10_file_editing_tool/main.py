"""Lesson 10: file-editing tool with small, safe patches.

Coding agents need to edit files, but they should not get unlimited write
access. This lesson adds a small edit tool that only writes inside the project
directory and only replaces one exact piece of text at a time.

This is still a fake model. The simplified stand-in for a real patch is an
exact old_text -> new_text replacement. Real coding agents usually create and
apply diffs, but the core idea is the same: validate the requested path, make a
small change, and return an observation to the transcript.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRATCH_FILE = PROJECT_ROOT / "lessons/10_file_editing_tool/scratch_note.txt"


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


@dataclass(frozen=True)
class EditRequest:
    path: str
    old_text: str
    new_text: str


def make_message(content: str) -> str:
    return json.dumps({"type": "message", "role": "assistant", "content": content})


def make_tool_call(name: str, argument: str) -> str:
    return json.dumps({"type": "tool_call", "name": name, "argument": argument})


def make_edit_argument(path: str, old_text: str, new_text: str) -> str:
    return json.dumps({"path": path, "old_text": old_text, "new_text": new_text})


def fake_model(transcript: list[Message]) -> str:
    latest_message = transcript[-1]
    latest_text = latest_message.content.lower()

    if latest_message.role == "tool":
        return make_message(f"Edit result:\n{latest_message.content}")

    if latest_message.role != "user":
        return make_message("I am waiting for a user request.")

    if "mark scratch done" in latest_text:
        argument = make_edit_argument(
            path="lessons/10_file_editing_tool/scratch_note.txt",
            old_text="status = draft",
            new_text="status = done",
        )
        return make_tool_call("replace_text", argument)

    if "change missing text" in latest_text:
        argument = make_edit_argument(
            path="lessons/10_file_editing_tool/scratch_note.txt",
            old_text="status = missing",
            new_text="status = done",
        )
        return make_tool_call("replace_text", argument)

    if "change learner to my name" in latest_text:
        argument = make_edit_argument(
                path="lessons/10_file_editing_tool/scratch_note.txt",
                old_text="owner = learner",
                new_text="owner = Emmanuel",
        )
        return make_tool_call("replace_text", argument)

    if "edit outside" in latest_text:
        argument = make_edit_argument(
            path="../README.md",
            old_text="Building AI Agents",
            new_text="Edited outside project",
        )
        return make_tool_call("replace_text", argument)

    return make_message("I do not need to edit a file for that.")


def parse_model_output(raw_output: str) -> Message | ToolCall:
    data = json.loads(raw_output)

    if data["type"] == "tool_call":
        return ToolCall(name=data["name"], argument=data["argument"])

    if data["type"] == "message":
        return Message(role=data["role"], content=data["content"])

    raise ValueError(f"Unknown model output type: {data['type']}")


def parse_edit_request(argument: str) -> EditRequest | str:
    try:
        data = json.loads(argument)
    except json.JSONDecodeError:
        return "Bad edit request: argument must be JSON."

    required_keys = {"path", "old_text", "new_text"}
    if set(data) != required_keys:
        return "Bad edit request: expected path, old_text, and new_text."

    if not all(isinstance(data[key], str) for key in required_keys):
        return "Bad edit request: path, old_text, and new_text must be strings."

    if not data["path"].strip():
        return "Bad edit request: path cannot be empty."

    if not data["old_text"]:
        return "Bad edit request: old_text cannot be empty."

    if data["old_text"] == data["new_text"]:
        return "Bad edit request: old_text and new_text are the same."
    
    if (data["new_text"] == "owner = Emmanuel") and ("scratch_note.txt" not in data["path"].split('/')):
        return "Bad edit request: Requested file is out of scope"

    return EditRequest(
        path=data["path"],
        old_text=data["old_text"],
        new_text=data["new_text"],
    )


def safe_project_path(path_text: str) -> Path | None:
    requested_path = (PROJECT_ROOT / path_text).resolve()

    if requested_path == PROJECT_ROOT:
        return None

    if PROJECT_ROOT not in requested_path.parents:
        return None

    return requested_path


def replace_text(argument: str) -> str:
    edit_request = parse_edit_request(argument)
    if isinstance(edit_request, str):
        return edit_request

    path = safe_project_path(edit_request.path)
    if path is None:
        return f"Blocked path: {edit_request.path}"

    if not path.exists():
        return f"File not found: {edit_request.path}"

    if not path.is_file():
        return f"Not a file: {edit_request.path}"

    content = path.read_text(encoding="utf-8")
    match_count = content.count(edit_request.old_text)

    if match_count == 0:
        return f"Text not found in {edit_request.path}: {edit_request.old_text!r}"

    if match_count > 1:
        return f"Text is not unique in {edit_request.path}: {edit_request.old_text!r}"

    updated_content = content.replace(edit_request.old_text, edit_request.new_text, 1)
    path.write_text(updated_content, encoding="utf-8")

    return f"Updated {edit_request.path}: {edit_request.old_text!r} -> {edit_request.new_text!r}"


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


def reset_scratch_file() -> None:
    SCRATCH_FILE.write_text(
        "title = file editing lesson\n"
        "status = draft\n"
        "owner = learner\n",
        encoding="utf-8",
    )


def main() -> None:
    reset_scratch_file()

    transcript: list[Message] = []
    tools = {"replace_text": replace_text}

    prompts = [
        "Mark scratch done",
        "Change missing text",
        "Edit outside the project",
    ]

    # for prompt in prompts:
    #     print(f"\nUSER: {prompt}")
    #     run_turn(transcript, prompt, tools)

    # print()
    # print("SCRATCH FILE NOW:")
    # print(SCRATCH_FILE.read_text(encoding="utf-8"))

    # print()
    # print_transcript(transcript)

    # TODO: Add a prompt that changes "owner = learner" to your name.
    prompts.append("change learner to my name")
    
    for prompt in prompts[3:]:
        print(f"\nUSER: {prompt}")
        run_turn(transcript, prompt, tools)

    print()
    print("SCRATCH FILE NOW:")
    print(SCRATCH_FILE.read_text(encoding="utf-8"))

    print()
    print_transcript(transcript)
    # TODO: Teach fake_model how to request that edit.
    # TODO: Add one more blocked edit example.


if __name__ == "__main__":
    main()
