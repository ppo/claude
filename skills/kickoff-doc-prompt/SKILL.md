---
name: kickoff-doc-prompt
description: Writes the prompt that starts a project's kickoff docs (`<repo>/docs/kickoff/_kickoff-doc-prompt.md`). The user pastes it into a fresh Claude session, which analyzes the project, interviews the user, and writes the docs – the vision plus first-version specifications – without writing code. First version only – stops if `docs/kickoff/` already holds anything. Not for writing the docs themselves, nor for updating existing ones (that's kickoff-doc-update).
disable-model-invocation: true
---

# Kickoff Doc Prompt

Produces `_kickoff-doc-prompt.md`: a self-contained prompt that turns a fresh session into the user's product analyst and architect for one project. That session reads the project's context, interviews the user, then writes a **vision** (broad, shallow) and **first-version specs** (narrow, deep).

You write the prompt, not the specs. Its quality comes from how well it is tailored to the project: its scope, its first-version target, and its one-way doors.


## Sources of Truth

Each thing is defined in one place; everywhere else points to it.

- [`template.md`](template.md) – what the prompt says, and how to fill it (its comments).
- [`conventions.md`](conventions.md) – how the docs are written: structure, navigation, legend, marks and IDs, page contents, writing rules. Versioned by its `Version:` line. Every project gets a copy at `<repo>/docs/kickoff/_conventions.md`, which records the version its docs follow. The prompt follows their typography, not their voice rule: it is the user speaking to the session, so "I", "me" and "you" belong there. Bringing existing docs to a newer version is the `kickoff-doc-update` skill's job, not this one's.
- [`check.py`](check.py) – checks a docs folder against `conventions.md`: `python3 <this skill's folder>/check.py <repo>/docs/kickoff`. Problems break a rule; warnings are heuristics to look at. This skill doesn't run it – there are no docs yet: the prompt has the session run it, with the absolute path of this skill's folder.
- [`methodology.md`](methodology.md) – how the user thinks and works, and their environment. This one is Pascal's: another user replaces it with their own. Every project gets a copy at `<repo>/.GI/context/methodology.md`. The prompt has the session read it first, so the prompt doesn't repeat it.
- This file – where things are, and how to write the prompt.


## Repo Layout

- `<repo>/.GI/context/` – the project's context: any files that help understand it (`.GI` is meant to be globally git-ignored).
- `<repo>/docs/kickoff/` – the prompt, the copy of the conventions, and the docs the session writes.
- Sibling folders – often related sub-projects, with earlier code or docs. Ex: in `~/dev/<project>/`, the repo `<project>-web` sits next to `<project>-cli` and `<project>-prototype`.

The session starts in the repo, usually with no memory: the prompt uses absolute paths.


## Workflow

1. **Locate.** Confirm the repo path; if the user gave none, ask. If `docs/kickoff/` exists and isn't empty, say so and stop: this skill only writes the first version. The user checks that folder, then deletes it or says how to go on (bringing existing docs to a newer version is `kickoff-doc-update`'s job). Otherwise, list `.GI/context/` and the sibling folders.
2. **Read the context, really.** Read the context files enough to know the project's intent, its sub-pages, its open questions (❓) and to-dos (🔴), its abandoned directions, and anything AI-generated (to be questioned). Look at existing code or prototypes: stack, data model, what's settled, what was a shortcut. Note related projects whose docs could be useful background.
3. **Characterize the project.** Personal tool vs public product/business; CLI vs app vs platform; greenfield vs successor of existing scripts. This changes the stakeholders, the constraints and the one-way doors.
4. **Fill the template**, following its comments. The scope, the first-version target and the one-way doors are the heart of the prompt: spend your thinking there.
5. **Copy the conventions** with `cp <this skill's folder>/conventions.md <repo>/docs/kickoff/_conventions.md` – never retyped: the copy must be byte-identical, emoji variation selectors included.
6. **Ensure the methodology file.** If `<repo>/.GI/context/methodology.md` is missing or differs from [`methodology.md`](methodology.md), propose the copy command to the user, who runs it.
7. **Report briefly**: where the prompt is, what's specific to this project, which guesses the user should check (first-version target, anything uncertain), and any fixed part you changed. Offer nothing they didn't ask for.


## Quality Checks

- Every `<…>` is filled and every comment deleted.
- The `check.py` path in the prompt is absolute, and the file is there.
- The fixed parts are unchanged – or changed on purpose, and said in the report.
- Tailored, not generic: the first-version target is explicit or explicitly open; the one-way doors, spikes and examples come from this project; each source in the reading list says what it's for.
- Nothing contradicts the methodology or the conventions, and the prompt repeats neither.
