# Building AI Agents: Hands-On Foundations

This workspace is a practical path for learning agents from first principles.
It starts without external APIs so you can understand the mechanics before adding a real model.

## Learning Path

1. `01_prompt_response`: call a tiny fake model and inspect inputs/outputs.
2. `02_tools`: expose Python functions as tools the model can request.
3. `03_agent_loop`: build the core loop: think, act, observe, answer.
4. `04_memory`: persist small pieces of useful information between runs.
5. `05_rag`: retrieve relevant notes before answering.
6. `06_messages`: represent a turn as explicit user, tool, and assistant messages.
7. `07_multi_turn_transcript`: keep one transcript across multiple user turns.
8. `08_command_tool`: run only allowlisted shell commands through a tool.
9. `09_file_reading_tool`: read project files through a path-safe tool.

See `ROADMAP.md` for the path from these fundamentals to a hands-on multi-agent coding assistant.

## Requirements

- Python 3.10+
- No third-party packages required for the first pass.

## How To Run

Run each lesson from the repo root:

```bash
python3 lessons/01_prompt_response/main.py
python3 lessons/02_tools/main.py
python3 lessons/03_agent_loop/main.py
python3 lessons/04_memory/main.py
python3 lessons/05_rag/main.py
python3 lessons/06_messages/main.py
python3 lessons/07_multi_turn_transcript/main.py
python3 lessons/08_command_tool/main.py
python3 lessons/09_file_reading_tool/main.py
```

## How To Learn

For each lesson:

1. Run the file once.
2. Read the `main.py` file.
3. Complete the `TODO` comments.
4. Run it again and compare behavior.

The goal is not to memorize a framework. The goal is to understand the moving parts that every agent framework wraps.
