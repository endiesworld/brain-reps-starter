# Python Engineering Track Instructions

## Purpose

This track teaches the user how to design and write Python functions, classes,
data structures, algorithms, and small systems at the level expected from an
intermediate to proficient Python software engineer.

## Relationship To The Agent Track

The main `lessons/` path teaches AI agent mechanics.

This `practice/python_engineering/` path teaches the general software
engineering skills needed to build those agents well:

- function boundaries
- data modeling
- algorithmic thinking
- validation
- error boundaries
- class and interface design
- small system design
- testing and refactoring

## Teaching Mode

This track must be 100% hands-on and exercise-first.

Do not give the user full solutions inside starter lessons. Instead, provide:

- a concrete problem
- clear expected behavior
- starter functions or classes
- failing `assert` checks
- TODO blocks
- runnable scripts
- stretch goals

The user should run the file, observe failures, implement the missing code, run
again, and ask for review after attempting the work.

## Lesson Style

Each lesson should usually contain:

- `README.md`: short problem statement, constraints, run command, stretch goals
- `main.py`: starter code with TODOs and assertions

Explanations should support the exercise, not replace it.

## Difficulty

Assume the user wants to grow beyond beginner Python.

Lessons should be beginner-accessible in setup, but they should train real
engineering judgment:

- choose honest function names
- separate pure logic from side effects
- validate inputs at boundaries
- make data shape explicit
- avoid overengineering
- write code that is easy to test

## Verification

After creating or editing a practice lesson, run it with `python3` when
practical. For starter exercises, failing assertions are acceptable when they
are the intended learning mechanism.
