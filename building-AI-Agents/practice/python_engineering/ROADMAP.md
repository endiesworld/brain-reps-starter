# Python Engineering Roadmap

## Destination

Build the software engineering foundation needed to design reliable Python
programs and agent runtimes: functions, data structures, algorithms, classes,
interfaces, and small systems.

## Track Rules

- Lessons are exercise-first.
- Starter code should contain TODOs, not complete solutions.
- Assertions define expected behavior.
- The user implements first, then asks for review.
- Prefer practical engineering problems over abstract puzzles.
- Keep each lesson runnable with `python3`.

## Lessons

- [ ] `01_function_design_dotenv`: Design a small `.env` parser and loader by
  separating parsing, validation, and side effects.
- [ ] `02_data_modeling_transcript`: Model user, assistant, and tool messages
  with dataclasses and small helper functions.
- [ ] `03_collections_tool_registry`: Use dictionaries, sets, and tuples to
  build a tool registry with lookup and validation.
- [ ] `04_algorithms_file_scanner`: Scan a small file tree, filter paths, count
  extensions, and sort results.
- [ ] `05_parsing_validation_commands`: Parse command strings and validate them
  against an allowlist.
- [ ] `06_error_boundaries`: Convert low-level exceptions into useful boundary
  errors without hiding bugs.
- [ ] `07_object_design_agent_runtime`: Decide when a class is useful by
  building a small stateful runtime.
- [ ] `08_interfaces_model_providers`: Design swappable model providers using
  simple interfaces.
- [ ] `09_system_design_task_queue`: Build a small in-memory task queue with
  status transitions.
- [ ] `10_testing_refactoring`: Refactor a messy implementation while preserving
  behavior with tests.

## First Lesson Agreement

The first lesson should be `01_function_design_dotenv`.

It should be based on the `.env` loader problem from lesson 12, but it should
not give away the final implementation. The user should implement functions
such as:

- `is_ignored_line`
- `parse_env_line`
- `load_env_values`
- `apply_env_values`

The lesson should demonstrate the difference between pure parsing functions and
side-effect functions that mutate `os.environ`.
