"""Lesson 04: memory.

Memory is state outside the current prompt.
This example stores simple preferences in a local JSON file.
"""

import json
from pathlib import Path


MEMORY_PATH = Path(__file__).with_name("memory.json")


def load_memory() -> dict[str, str]:
    if not MEMORY_PATH.exists():
        return {}
    return json.loads(MEMORY_PATH.read_text())


def save_memory(memory: dict[str, str]) -> None:
    MEMORY_PATH.write_text(json.dumps(memory, indent=2) + "\n")


def respond(user_prompt: str, memory: dict[str, str]) -> str:
    lower = user_prompt.lower()

    if lower.startswith("remember "):
        fact = user_prompt.removeprefix("remember ").strip()
        key, _, value = fact.partition("=")
        if not key or not value:
            return "Use the format: remember key=value"
        memory[key.strip()] = value.strip()
        save_memory(memory)
        return f"Remembered {key.strip()}."

    if "my name" in lower and "name" in memory:
        return f"Your name is {memory['name']}."

    return "I do not know yet. Teach me with: remember name=Your Name"


def main() -> None:
    memory = load_memory()

    prompts = [
        "remember name=Ada",
        "What is my name?",
    ]

    for prompt in prompts:
        print("USER:", prompt)
        print("ASSISTANT:", respond(prompt, memory))

    # TODO: Store another memory key, like city=London.
    # TODO: Update respond so it can answer "What city am I in?"


if __name__ == "__main__":
    main()

