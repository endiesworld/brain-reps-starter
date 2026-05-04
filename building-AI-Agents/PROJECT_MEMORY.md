# Project Memory

## Purpose

This project exists to teach the user everything about building AI agents, starting from the fundamentals and progressing toward advanced agent systems.

## Objective

The user's destination is to build a multi-agent coding application similar in ambition to Claude Code and Codex.

## Operating Mode

The learning structure should be 100% hands-on. The repo should evolve through runnable code, exercises, experiments, and incremental implementation.

## Current Focus

We are tightening the beginner lessons so they teach the intended concept honestly and clearly.

The next planning task is shaping the path from the existing fundamentals toward a hands-on multi-agent coding app.

## Recent Cleanup

`lessons/05_rag/main.py` now separates scoring, retrieval, prompt building, and draft answering. It explicitly states that no real model call happens yet.

Lessons 1-3 were reviewed and cleaned so function names, return annotations, and TODOs match the actual behavior. Lesson 4 ran successfully without needing changes.

`lessons/06_messages/main.py` was added as the first Phase 2 lesson. It introduces explicit `Message` objects, `ToolCall` objects, a one-turn transcript, and a tool observation message.

`lessons/07_multi_turn_transcript/main.py` was added to keep one transcript across multiple user turns. It shows the model using earlier tool messages to answer a later user question.

## Next Learning Step

Add a command-running tool with a strict allowlist. This starts the path toward a coding agent that can inspect and verify a repo without giving it arbitrary shell access.

## Durable Decisions

- The repo should favor clear learning over clever code.
- Lessons should be runnable and small.
- Each lesson should teach one main concept.
- Simplified examples are acceptable only when the simplification is explicit.
- Future work should preserve the path from fundamentals to multi-agent coding systems.
