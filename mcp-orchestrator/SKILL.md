---
name: mcp-orchestrator
description: Use whenever the user wants to tackle a substantial feature request, refactor, or multi-part coding task by delegating pieces to other AI tools registered as MCP servers (e.g. Codex CLI instances, other Claude instances, Gemini) instead of doing all implementation as a single agent. Trigger for phrases like "orchestrate this across my agents", "delegate this to my codex workers", "split this feature across models", "act as the manager and dispatch subtasks", "use my registered MCP workers for this", or any request implying role separation between a planning/reviewing Claude and specialized implementer tools. Also trigger if the user mentions running `claude mcp add` for tools like codex-review, codex-refactor, codex-tests, or similar workers and wants a task run through them. Do NOT trigger for simple single-file edits, one-step tasks, or work that isn't naturally split into independently-dispatchable pieces — just do those directly.
---

# MCP Multi-Agent Orchestration

Claude acts as the **manager**: it plans, decomposes a request into subtasks, dispatches each subtask to a specialized worker tool registered over MCP, reviews what comes back, resolves conflicts, and merges the result. Workers implement; Claude reasons, plans, and is accountable for the final output.

This only makes sense for tasks big enough to benefit from parallel, role-separated work. A single-file bug fix doesn't need a manager — just fix it.

## Step 1: Figure out the environment

Behavior differs depending on where this is running, so check first:

- **Claude Code / terminal environment**: real subprocess-backed MCP servers can be registered with `claude mcp add <name> -- <command>`, and Claude has direct terminal + file access to verify worker output (run tests, diff files, lint).
- **This chat interface (claude.ai app)**: MCP servers show up as connected tools in the tool list, typically tagged `[third_party_mcp_app]` for consumer connectors, or as plain named tools for things like Notion/Figma. There's no terminal to independently verify a worker's code changes — verification has to lean on what the worker itself reports back, plus Claude's own read of the diffs/output it returns.

If unsure which environment you're in, it's usually obvious from what tools are available — if `bash_tool` and a real filesystem are present, treat it as the Claude Code case even if technically running in Claude.ai's VM.

## Step 2: Ask the user which workers are registered

Don't guess or assume fixed roles like "frontend/backend/tests" — every user's setup is different. At the start of a session (or when the user first invokes this skill), ask:

1. What MCP workers do you have registered right now? (names, e.g. `codex-review`, `codex-refactor`, `codex-tests`, or connected tools visible in the tool list)
2. What role should each one play for this task? (e.g. "codex-refactor does the implementation," "codex-tests writes and runs the test suite," "codex-review does a second-pass code review")

If the user says they don't have any workers registered yet, or the ones they name aren't actually available:

- **In Claude Code**: offer to generate the `claude mcp add` commands for the roles this task needs, e.g.:
  ```bash
  claude mcp add codex-refactor -- codex mcp-server
  claude mcp add codex-tests -- codex mcp-server
  ```
  Let the user run these (or run them via bash_tool if you have permission), then proceed once they confirm the servers are up.
- **In this chat interface**: check the tool list for already-connected MCP servers that could plausibly fill each role. If none fit, use `search_mcp_registry` and `suggest_connectors` to let the user connect something suitable, rather than picking a worker for them.

Only fall back to doing the task yourself as a single agent, with a note that no workers were available, if the user explicitly says they don't want to set anything up right now.

## Step 3: Plan and decompose

Before dispatching anything, write out a short plan:

- What are the independent subtasks? (independent = a worker can complete it without waiting on another worker's output)
- Which registered worker does each subtask map to?
- What's the shared context each worker needs (relevant files, conventions, interfaces/contracts between the pieces so frontend and backend work don't diverge)?
- What does "done" look like for each subtask, concretely enough that Claude can check it later?

Share this plan with the user briefly before dispatching, especially for anything non-trivial — a one-line "here's the breakdown" is enough, not a full report.

## Step 4: Dispatch

Call each worker's MCP tool with a self-contained prompt: the subtask, the shared context/contracts from Step 3, and what output format you expect back (a diff, a file, a test report, etc.). Don't assume workers share context with each other — anything one worker's output depends on from another worker's output must be included explicitly, which usually means dispatching in dependency order rather than all at once when there's a real interface dependency (e.g. backend API shape needs to exist before frontend can consume it). Independent subtasks (e.g. "write tests" vs "implement feature," if they're working off an agreed interface) can go out in parallel.

## Step 5: Review and reconcile

This is Claude's core job in this loop — don't just relay worker output verbatim.

- Read what each worker produced. Check it against the "done" criteria from Step 3.
- If in Claude Code, actually verify: run the tests a worker wrote, check that the implementation a worker produced actually compiles/lints, diff files for unexpected scope creep.
- If workers disagree or their outputs conflict (e.g. two different assumptions about a shared interface), resolve it yourself — decide which is correct, or synthesize a fix — rather than surfacing the conflict to the user first. The user should see a coherent merged result plus a short explanation of any judgment call you made, not raw disagreement between tools.
- If a worker's output fails verification, decide whether to send it back to the same worker with corrective feedback, dispatch to a different worker, or fix it directly yourself if it's a small issue not worth another round trip.

## Step 6: Merge and present

Present the user with the merged, working result — not a transcript of every worker exchange. Mention:

- What was delegated to what worker (briefly)
- Any judgment calls made while reconciling conflicting outputs
- What's still open or needs the user's decision, if anything

Keep the play-by-play out of the final summary unless the user wants to see the detailed back-and-forth — offer to show it if useful, but don't dump it by default.

## Notes on scaling this

- This pattern is overkill for small tasks. If a subtask breakdown ends up being one subtask, just do the work directly instead of ceremonially "dispatching to a worker" for a single-item plan.
- Different models genuinely have different strengths (e.g. one may be stronger at isolated sandboxed coding, another at long-context or multimodal input) — when the user hasn't specified roles precisely, it's fine to suggest a role split based on what's known about the registered tools, but confirm with the user rather than silently assuming.
- Reference: MCP spec at https://modelcontextprotocol.io and the server registry at https://github.com/modelcontextprotocol/servers, if the user needs help finding or understanding a specific worker tool to register.
