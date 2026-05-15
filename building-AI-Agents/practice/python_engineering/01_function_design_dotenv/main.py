"""
Practice Session 01: Function Design With .env Files

Run:
    python3 python_engineering/01_function_design_dotenv/main.py

This file starts with TODOs and failing assertions on purpose.
Implement one function at a time, then run the file again.
"""


def is_ignored_line(line):
    """Return True when a .env line should be skipped."""
    # TODO:
    # - strip whitespace from the line
    line = line.strip()
    # - ignore empty lines
    if not line:
        return True
    # - ignore lines that start with "#"
    if line.startswith("#"):
        return True
    return False


def parse_env_line(line):
    """Parse one KEY=value line into a (key, value) tuple."""
    # TODO:
    # - reject ignored lines by raising ValueError
    if is_ignored_line(line):
        raise ValueError("Ignored lines cannot be parsed")
    # - require exactly the shape KEY=value
    if '=' not in line:
        raise ValueError("Data not in the right format")
    line = line.split('=')
    # - strip whitespace around the key and value
    key = line[0].strip()
    value = line[1].strip()
    # - strip matching single or double quotes around the value
    value = value.strip("'")
    value = value.strip('"')
    return (key, value)


def load_env_values(lines):
    """Parse many .env lines into a dictionary without mutating anything."""
    # TODO:
    # - skip ignored lines
    results = {}
    for line in lines:
        try:
            key, value = parse_env_line(line)
            results[key] = value
        except ValueError:
            continue
    # - parse every other line
    # - return a dictionary of key/value pairs
    return results


def apply_env_values(values, environ):
    """Apply parsed values to an environment-like dictionary."""
    # TODO:
    # - mutate the provided environ dictionary
    for key in values.keys():
        environ[key] = values[key]
    # - do not return a new dictionary
    return None


def run_checks():
    assert is_ignored_line("") is True
    assert is_ignored_line("   ") is True
    assert is_ignored_line("# comment") is True
    assert is_ignored_line("  # comment with leading space") is True
    assert is_ignored_line("API_KEY=abc123") is False

    assert parse_env_line("API_KEY=abc123") == ("API_KEY", "abc123")
    assert parse_env_line(" MODEL = gpt-5 ") == ("MODEL", "gpt-5")
    assert parse_env_line("NAME='Ada Lovelace'") == ("NAME", "Ada Lovelace")
    assert parse_env_line('GREETING="hello world"') == ("GREETING", "hello world")

    try:
        parse_env_line("# ignored")
    except ValueError:
        pass
    else:
        raise AssertionError("parse_env_line should reject ignored lines")

    try:
        parse_env_line("MISSING_EQUALS")
    except ValueError:
        pass
    else:
        raise AssertionError("parse_env_line should reject invalid lines")

    lines = [
        "# local settings",
        "",
        "API_KEY=abc123",
        "MODEL=gpt-5",
        "OWNER='Grace Hopper'",
    ]
    values = load_env_values(lines)

    assert values == {
        "API_KEY": "abc123",
        "MODEL": "gpt-5",
        "OWNER": "Grace Hopper",
    }

    fake_environ = {"EXISTING": "keep-me"}
    result = apply_env_values(values, fake_environ)

    assert result is None
    assert fake_environ == {
        "EXISTING": "keep-me",
        "API_KEY": "abc123",
        "MODEL": "gpt-5",
        "OWNER": "Grace Hopper",
    }

    print("All checks passed.")


if __name__ == "__main__":
    run_checks()
