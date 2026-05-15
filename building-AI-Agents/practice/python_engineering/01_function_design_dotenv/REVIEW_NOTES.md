# Review Notes

## Status

The current implementation passes the starter checks:

```bash
python3 python_engineering/01_function_design_dotenv/main.py
```

Expected output:

```text
All checks passed.
```

## Findings To Revisit

1. `load_env_values` hides invalid `.env` lines.

   Current behavior catches every `ValueError` and continues. That means invalid
   non-ignored lines such as `BROKEN_LINE` are silently skipped.

   Better shape:

   ```python
   for line in lines:
       if is_ignored_line(line):
           continue
       key, value = parse_env_line(line)
       results[key] = value
   ```

2. `parse_env_line` should split only once.

   Current behavior uses `line.split("=")`, which loses data when the value
   contains another equals sign.

   Example:

   ```python
   parse_env_line("TOKEN=a=b=c")
   ```

   Prefer:

   ```python
   key, value = line.split("=", 1)
   ```

3. Quote stripping is too broad.

   Current behavior strips quote characters from the outside even when they are
   not a matching pair. The lesson asks for matching single or double quotes.

   Better shape:

   ```python
   if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
       value = value[1:-1]
   ```

## Good Parts

- The function boundaries are clear.
- `is_ignored_line`, `parse_env_line`, `load_env_values`, and
  `apply_env_values` each have a focused responsibility.
- `apply_env_values` correctly mutates the provided dictionary and returns
  `None`.

## Suggested Next Session

Start by adding assertions for the three edge cases above, then update the
implementation until the new assertions pass.
