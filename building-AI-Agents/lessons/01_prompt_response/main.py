"""Lesson 01: prompt -> model -> response.

This is the smallest useful unit in agent development.
Before tools, memory, planning, or retrieval, you need to understand what
message you send to a model and what response you get back.
"""


def fake_model(system_prompt: str, user_prompt: str) -> str:
    """A deterministic stand-in for a real LLM call."""
    if "concise" in system_prompt.lower():
        return f"Short answer: {user_prompt[:45]}"
    return f"I received your request: {user_prompt}"


def run_prompt(system_prompt: str, user_prompt: str) -> None:
    response = fake_model(system_prompt, user_prompt)

    print("SYSTEM:", system_prompt)
    print("USER:", user_prompt)
    print("ASSISTANT:", response)


def main() -> None:
    system_prompt = "You are a concise assistant."
    user_prompt = "Explain what an AI agent is in one sentence."
    run_prompt(system_prompt, user_prompt)

    system_prompt = "You are a detailed assistant."
    user_prompt = "Explain what changes when the system prompt is not concise."
    run_prompt(system_prompt, user_prompt)

    # TODO: Add a third prompt pair and predict the fake model response before running it.

if __name__ == "__main__":
    main()
