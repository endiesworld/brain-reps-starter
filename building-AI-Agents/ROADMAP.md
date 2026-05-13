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
- [x] Add a command-running tool with a strict allowlist.
- [x] `09_file_reading_tool`: Add a file-reading tool with path safety.
- [x] `10_file_editing_tool`: Add a file-editing tool that writes small patches.
- [x] `11_failure_handling`: Add failure handling for missing tools, bad tool arguments, and max-step exhaustion.
- [ ] `12_real_model_loop`: Replace the fake model with a real model call while keeping local tool execution.

## Phase 3: Coding Agent Basics

- [ ] `13_repo_scanner`: Build a repo scanner that lists files and searches code.
- [ ] `14_code_question_answering`: Teach the agent to answer questions using retrieved code context.
- [ ] `15_patch_and_verify`: Teach the agent to propose a small patch and run a verification command after editing.

## Phase 4: Tool Protocols And Agent Graphs

- [ ] `16_mcp_intro`: Introduce MCP as a standard way to expose tools and resources.
- [ ] `17_custom_mcp_server`: Build a small custom MCP server for a local tool.
- [ ] `18_state_graphs`: Introduce graph-shaped agent control flow without a framework.
- [ ] `19_langgraph_single_agent`: Rebuild the single-agent loop with LangGraph.
- [ ] `20_langgraph_coding_agent`: Use LangGraph for a coding agent with tools and verification.

## Phase 5: Multi-Agent Coordination

- [ ] `21_multi_agent_roles`: Add explorer, worker, and reviewer roles with clear boundaries.
- [ ] `22_multi_agent_orchestrator`: Add an orchestrator that assigns work and merges results.

## Phase 6: Production Frameworks And App Shape

- [ ] `23_adk_intro`: Introduce ADK after the raw loop and graph concepts are understood.
- [ ] `24_adk_multi_agent_app`: Build a small ADK multi-agent coding workflow.
- [ ] `25_codex_like_cli`: Build a CLI around the orchestrator with session resume, approvals, project instructions, and final task reports.

## Rule For Every Step

Every roadmap item should become a runnable lesson or exercise. The user should edit code, run it, observe behavior, and then improve it.
