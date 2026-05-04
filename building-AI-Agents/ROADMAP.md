# Hands-On Agent Roadmap

## Destination

Build a local multi-agent coding assistant that can inspect a repo, plan work, edit files, run commands, observe results, and coordinate specialized agents.

## Phase 1: Single-Turn Foundations

- [x] Prompt, model stand-in, response
- [x] Tools as regular Python functions
- [x] Tool calls as structured data
- [x] Agent loop with action, observation, and final answer
- [x] File-backed memory
- [x] Basic retrieval over notes

## Phase 2: Stronger Local Agent Mechanics

- [x] Replace fake model decisions with explicit message objects.
- [x] Add a transcript so each turn can see prior user, assistant, tool, and observation messages.
- [ ] Add a command-running tool with a strict allowlist.
- [ ] Add a file-reading tool.
- [ ] Add a file-editing tool that writes small patches.
- [ ] Add failure handling for missing tools, bad tool arguments, and max-step exhaustion.

## Phase 3: Coding Agent Basics

- [ ] Build a repo scanner that lists files and searches code.
- [ ] Teach the agent to answer questions using retrieved code context.
- [ ] Teach the agent to propose a small patch.
- [ ] Teach the agent to run a verification command after editing.
- [ ] Store a task summary so the next run can continue.

## Phase 4: Multi-Agent Coordination

- [ ] Add an explorer agent that only reads and summarizes code.
- [ ] Add a worker agent that owns a small edit scope.
- [ ] Add a reviewer agent that checks the patch for bugs and missing tests.
- [ ] Add an orchestrator that assigns work and merges results.
- [ ] Add a shared project memory file for durable context.

## Phase 5: Codex-Like Application Shape

- [ ] Build a CLI interface around the orchestrator.
- [ ] Add session resume from saved transcripts.
- [ ] Add approval gates for risky commands and file writes.
- [ ] Add project-specific instructions from `AGENTS.md`.
- [ ] Add a final task report with changed files, commands run, and next steps.

## Rule For Every Step

Every roadmap item should become a runnable lesson or exercise. The user should edit code, run it, observe behavior, and then improve it.
