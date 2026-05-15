# Practice Session 01: Function Design With `.env` Files

## Goal

Build a tiny `.env` loader by separating pure functions from functions that
cause side effects.

This is a simplified stand-in for the kind of configuration loading used in
real applications and AI agent runtimes. It is intentionally small so the
function boundaries are easy to see.

## What You Will Practice

- Designing functions with clear responsibilities.
- Parsing text into structured values.
- Validating input before using it.
- Keeping pure logic separate from side effects.
- Using `assert` checks as a lightweight feedback loop.

## Problem

You will implement four functions in `main.py`:

- `is_ignored_line(line)`: returns `True` for blank lines and comments.
- `parse_env_line(line)`: turns one `KEY=value` line into a `(key, value)` tuple.
- `load_env_values(lines)`: reads many lines and returns a dictionary.
- `apply_env_values(values, environ)`: writes parsed values into an environment-like dictionary.

The important design idea:

- parsing functions should not mutate anything
- the apply function is where mutation happens

## Run It

From the repo root:

```bash
python3 practice/python_engineering/01_function_design_dotenv/main.py
```

Or from this `practice/` directory:

```bash
python3 python_engineering/01_function_design_dotenv/main.py
```

The first run should fail. That is expected. Implement one TODO at a time and
run the file again after each change.

## Rules

- Do not import a dotenv package.
- Keep each function focused on its own job.
- Do not mutate `os.environ` in this lesson.
- Use the provided assertions as the required behavior.

## Stretch Goals

After the assertions pass:

- Add support for `export KEY=value`.
- Reject empty keys like `=value`.
- Decide whether inline comments such as `KEY=value # comment` should be supported.
- Add your own assertions for edge cases.
