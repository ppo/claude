---
name: kickoff-prompt
description: Writes a kickoff prompt that Pascal pastes into a fresh Claude session so that session analyzes one of his projects, interviews him, and writes the vision plus first-version specifications – without writing code. Use when Pascal asks to "write a prompt" / "initial prompt" / "kickoff prompt" for a project or repo, to "do the same for {project}" after such a prompt, or wants a session to "analyze what I want and write the specs". Not for writing the specs themselves.
---

# Kickoff Prompt

Produces `<repo>/docs.claude/_initial-prompt.md`: a self-contained prompt that turns a fresh session into Pascal's product analyst and architect for one project. That session reads his context, interviews him, then writes a **vision** (broad, shallow) and **first-version specs** (narrow, deep) into `<repo>/docs.claude/`.

You write the prompt, not the specs. The quality of the prompt comes from how well it is tailored to the project: its scope, its first-version target, and its one-way doors.


## Conventions

- **Repo layout** – `<repo>/.GI/ContextFiles/` holds Pascal's context (Notion exports, `<Name>.<YYMMDD>.txt|md`; `.GI` = his global git-ignore). `<repo>/docs.claude/` is where Claude-written docs go. Sibling folders (ex: `../<name>-cli`, `../<name>-prototype`) often hold earlier code.
- **Methodology** – [`assets/Methodology.md`](assets/Methodology.md) is the canonical description of how Pascal thinks and works. Every project gets a copy at `<repo>/.GI/ContextFiles/Methodology.md`, and every prompt tells the session to read it first.
- **Self-contained** – the target session starts in the project repo, usually with no memory. Use absolute paths, and keep the essentials of Pascal's constraints in the prompt itself (the methodology file has the rest).
- **His writing conventions** – en dash ` – ` in prose, Title Case headings, TSV never CSV, review protocol 🤠 / 🧞‍♂️ / 🪤.


## Workflow

1. **Locate.** Confirm the repo path. List `.GI/ContextFiles/`, `docs.claude/` (it may already hold a prompt or docs) and sibling folders. If Pascal gave no repo, ask.
2. **Read the context, really.** Read the context files enough to know the project's intent, its sub-pages, its open ❓, its abandoned directions, and anything AI-generated (to be questioned). Look at existing code or prototypes: stack, data model, what's settled, what was a shortcut. Note related projects (Andy, Andy CLI, others) whose docs could be useful background.
3. **Characterize the project.** Personal tool vs public product/business; CLI vs app vs platform; greenfield vs successor of existing scripts. This changes the stakeholders, the constraints (offline-first for him vs online product), and the one-way doors.
4. **Decide the scope**, the heart of the prompt:
   - **Vision** – what "the whole" covers for this project, in one sentence of parts.
   - **First version** – the smallest thing he'd *actually use* (or that moves a business forward), plus a path to grow. If the context makes it clear, state it. If not, state your best guess **and** tell the session to confirm it first – or list 2–3 candidates from his notes. Never silently pick.
5. **List the likely one-way doors** for this project (4–7), each with the real options or tensions from his notes. Always consider: build vs adopt (name the actual alternatives he looked at or that exist), source of truth & data format, identifiers, platform/stack, public interfaces (CLI grammar, plugin contract, API), migration from what he uses today, and – for public products – neutrality, legal, privacy, money.
6. **Fill the template** from [`references/template.md`](references/template.md). Tailor every `<…>` and remove guidance comments. Keep the fixed parts (interview rules, writing rules, phases) unless the project calls for a change.
7. **Ensure the methodology file.** If `<repo>/.GI/ContextFiles/Methodology.md` is missing or differs from `assets/Methodology.md`, propose the copy command to Pascal (he runs commands himself).
8. **Report briefly**: where the prompt is, what's specific to this project, and which guesses he should check (first-version target, anything uncertain). Offer nothing he didn't ask for.


## Quality Checks

- Scope has **two levels with different depths**, and the first-version target is explicit or explicitly open.
- Reading list uses **absolute paths**, says what each source is for, and marks other projects' docs as **background only – don't modify**.
- One-way doors are **specific to this project**, not generic filler.
- Ideas from his notes are to be **sorted (first version / later / never)**, not all specified.
- The session **writes no code, commits nothing, installs nothing**, changes only `docs.claude/`, and **pauses between phases**.
- Nothing in the prompt contradicts [`assets/Methodology.md`](assets/Methodology.md).
