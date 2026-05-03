"""Lesson 02: tools.

Tools are regular code functions that an agent can call.
The model does not magically access your computer; you decide which tools exist.
"""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


def calculator(expression: str) -> str:
    """Evaluate a small arithmetic expression.

    This intentionally supports only simple arithmetic characters.
    Never pass arbitrary user text into eval in a production agent.
    """
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        return "Error: unsupported expression"
    return str(eval(expression, {"__builtins__": {}}, {}))


def uppercase(text: str) -> str:
    return text.upper()


def fake_model(user_prompt: str) -> ToolCall | str:
    """Return either a final answer or a requested tool call."""
    if "calculate" in user_prompt.lower():
        expression = user_prompt.lower().split("calculate", 1)[1].strip()
        return ToolCall(name="calculator", argument=expression)
    elif "uppercase" in user_prompt.lower():
        text = user_prompt.lower().split("uppercase", 1)[1].strip()
        return ToolCall(name="uppercase", argument=text)
    return "No tool needed. I can answer directly."


def run_turn(user_prompt: str, tools: dict[str, Callable[[str], str]]) -> None:
    """Run one user prompt through the fake model and any requested tool."""
    model_output = fake_model(user_prompt)

    print("USER:", user_prompt)
    print("MODEL OUTPUT:", model_output)

    if isinstance(model_output, ToolCall):
        tool = tools[model_output.name]
        observation = tool(model_output.argument)
        print("TOOL OBSERVATION:", observation)
    else:
        print("ASSISTANT:", model_output)


def main() -> None:
    tools: dict[str, Callable[[str], str]] = {
        "calculator": calculator,
        "uppercase": uppercase,
    }

    user_prompt = "Calculate 12 * (4 + 3)"
    run_turn(user_prompt, tools)

    user_prompt = "Uppercase hello world"
    run_turn(user_prompt, tools)

    # TODO: Add another tool named "word_count" and teach fake_model when to call it.


if __name__ == "__main__":
    main()
