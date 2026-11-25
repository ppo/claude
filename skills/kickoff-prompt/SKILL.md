---
name: kickoff-prompt
description: Writes a kickoff prompt that the user pastes into a fresh Claude session, so that session analyzes one of their projects, interviews them, and writes the vision plus first-version specifications – without writing code. Not for writing the specs themselves.
disable-model-invocation: true
---

# Kickoff Prompt

Produces `_kickoff-prompt.md`: a self-contained prompt that turns a fresh session into the user's product analyst and architect for one project. That session reads the project's context, interviews the user, then writes a **vision** (broad, shallow) and **first-version specs** (narrow, deep).

You write the prompt, not the specs. Its quality comes from how well it is tailored to the project: its scope, its first-version target, and its one-way doors.


## Sources of Truth

Each thing is defined in one place; everywhere else points to it.

- [`template.md`](template.md) – what the prompt says, how to fill it (its comments), and the conventions of the docs the session writes: structure, legend, decision format, writing rules. Follow those conventions in the prompt too.
- [`methodology.md`](methodology.md) – how the user thinks and works, and their environment. This one is Pascal's: another user replaces it with their own. Every project gets a copy at `<repo>/.GI/context/methodology.md`. The prompt has the session read it first, so the prompt doesn't repeat it.
- This file – where things are, and how to write the prompt.


## Repo Layout

- `<repo>/.GI/context/` – the project's context: any files that help understand it (`.GI` is meant to be globally git-ignored).
- `<repo>/docs/kickoff/` – the prompt, and the docs the session writes.
- Sibling folders – often related sub-projects, with earlier code or docs. Ex: in `~/dev/<project>/`, the repo `<project>-web` sits next to `<project>-cli` and `<project>-prototype`.

The session starts in the repo, usually with no memory: the prompt uses absolute paths.


## Workflow

1. **Locate.** Confirm the repo path. List `.GI/context/`, `docs/kickoff/` (it may already hold a prompt or docs) and sibling folders. If the user gave no repo, ask.
2. **Read the context, really.** Read the context files enough to know the project's intent, its sub-pages, its open questions (❓) and to-dos (🔴), its abandoned directions, and anything AI-generated (to be questioned). Look at existing code or prototypes: stack, data model, what's settled, what was a shortcut. Note related projects whose docs could be useful background.
3. **Characterize the project.** Personal tool vs public product/business; CLI vs app vs platform; greenfield vs successor of existing scripts. This changes the stakeholders, the constraints and the one-way doors.
4. **Fill the template**, following its comments. The scope, the first-version target and the one-way doors are the heart of the prompt: spend your thinking there.
5. **Ensure the methodology file.** If `<repo>/.GI/context/methodology.md` is missing or differs from [`methodology.md`](methodology.md), propose the copy command to the user, who runs it.
6. **Report briefly**: where the prompt is, what's specific to this project, which guesses the user should check (first-version target, anything uncertain), and any fixed part you changed. Offer nothing they didn't ask for.


## Quality Checks

- Every `<…>` is filled and every comment deleted; every `{…}` is kept.
- The fixed parts are unchanged – or changed on purpose, and said in the report.
- Tailored, not generic: the first-version target is explicit or explicitly open; the one-way doors, spikes and examples come from this project; each source in the reading list says what it's for.
- Nothing contradicts the methodology.
