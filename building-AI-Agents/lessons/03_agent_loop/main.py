"""Lesson 03: the agent loop.

An agent repeatedly:
1. asks the model what to do next
2. runs a tool if requested
3. feeds the observation back into the next step
4. stops when the model returns a final answer
"""

from dataclasses import dataclass
from typing import Callable
import re


@dataclass(frozen=True)
class ToolCall:
    name: str
    argument: str


@dataclass(frozen=True)
class FinalAnswer:
    text: str


def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        return "Error: unsupported expression"
    return str(eval(expression, {"__builtins__": {}}, {}))


def fake_model(goal: str, observations: list[str]) -> ToolCall | FinalAnswer:
    """A deterministic model policy for learning the loop mechanics."""
    if not observations:
        if "cost" in goal.lower():
            matches = re.findall(r"-?\d+\.?\d*", goal)
            if len(matches) < 2:
                return FinalAnswer(text="I need both the item count and price to calculate the cost.")

            items_and_cost = f"{matches[0]} * {matches[1]}"
            return ToolCall(name="calculator", argument=items_and_cost)
        return FinalAnswer(text="I can answer this without tools.")

    latest_observation = observations[-1]
    return FinalAnswer(text=f"The total cost is ${latest_observation}.")


def run_agent(goal: str, tools: dict[str, Callable[[str], str]], max_steps: int = 5) -> str:
    observations: list[str] = []

    for step in range(1, max_steps + 1):
        decision = fake_model(goal, observations)
        print(f"STEP {step}:", decision)

        if isinstance(decision, FinalAnswer):
            return decision.text

        if decision.name not in tools:
            return f"Error: unknown tool {decision.name!r}"

        observation = tools[decision.name](decision.argument)
        observations.append(observation)
        print("OBSERVATION:", observation)

    return "Error: reached max steps without a final answer"


def main() -> None:
    tools = {"calculator": calculator}
    goal = "What is the cost of 3 items at $19 each?"
    answer = run_agent(goal, tools)
    print("FINAL:", answer)

    print("SECOND GOAL")
    goal = "What is the cost of 8 items at $7 each?"
    answer = run_agent(goal, tools)
    print("FINAL:", answer)

    print("LOW MAX STEPS")
    goal = "What is the cost of 8 items at $7 each?"
    answer = run_agent(goal, tools, max_steps=1)
    print("FINAL:", answer)

    # TODO: Add a second tool and update fake_model so the loop can choose between tools.


if __name__ == "__main__":
    main()
