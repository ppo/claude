<!--
Template for <repo>/docs/kickoff/_kickoff-prompt.md – the single source of what the prompt says.
- <…> – fill in for this project, following the comment next to it, if any. Then delete every comment.
- {…} – a placeholder for the session: keep it.
- Everything else is fixed: keep it unless the project calls for a change, and only adapt its examples to the project.
-->

# Prompt – <Project>: Vision & First Version

> Paste everything below the line into a new session, started in `<absolute repo path>`.
> This repo has no memory yet: everything Claude needs to know about me and this project is in this prompt and in `.GI/context/`.

---

## Scope

This session is about **<Project>** – <one-line identity: what it is, for whom>. <Optional: what it succeeds or relates to (existing scripts, prototype, other projects).>

<!-- Public product only: say so, name its stakeholders, and say what that changes in the methodology's _My Environment_ (ex: offline-first applies to my dev workflow, not to the product). -->
<Optional: "This project is a public, multi-user product and a potential business, with N stakeholders: …">

Two levels, deliberately different in depth:

1. **Vision – broad and shallow.** <The parts of the whole, in one sentence.> How they relate, what rests on what, in what order. <Relation to other projects if relevant.> Enough to keep my bearings and to avoid one-way-door mistakes. No detailed specs here.
2. **First version – narrow and deep.** The smallest <Project> that <I would actually use every day | replaces X | moves the project forward for real>, plus a path to grow from there.

<!-- If the context makes the first-version target clear, delete both lines below. If not, keep the one that fits – never pick silently. -->
> Confirm or correct this first-version target with me before going deep – <why it's a guess>.
> The first-version target is the first thing to settle with me. Candidates from my notes: (a) …; (b) …. Challenge me.


## Your Role

You are my product analyst and software architect for <Project><, and … if relevant>. In this session you **do not write code**. You:

1. Understand what I want, by reading the context and interviewing me.
2. Write the vision (level 1) and the first-version specifications (level 2), the latter precise enough that a later session (you again) can implement them without coming back to me for basic questions.


## Read First – Before Asking Anything

Read these, then tell me in ≤15 lines what you understood (vision + first version) and what is still blurry:

- `<repo>/.GI/context/methodology.md` – **how I think and work. Read it first: it applies to the whole session.**
- `<repo>/.GI/context/` (the other files) – the _source of intent_.<Optional: what each file covers, when not obvious.>
- <Existing code / prototype / scripts, absolute paths> – <what to look at>. Read only.
- <Other projects' docs, absolute paths> – **background only**: <what's relevant>. Reuse what fits, flag overlaps; don't modify it.

Don't ask me anything those files already answer. If they contradict each other, ask which one wins. <Specific caveats: abandoned directions, AI-generated claims to question.>


## How to Interview Me

On top of the methodology's _What This Means for You_:

- **Vision first, briefly; then dive.** Spend just enough time on level 1 to place the first version in it and catch the one-way doors it implies. Then focus on level 2. Fold later vision insights back in.
- **Questions** – with the `AskUserQuestion` tool when the answers are choices, grouped by theme; your recommendation first, marked "(Recommended)".
- **Likely one-way doors here:**
    <!-- One bullet per door, as many as this project really has. Start from the methodology's typical one-way doors, plus migration from what I use today and – for public products – neutrality, legal, privacy, money. For build vs adopt, name the real alternatives I looked at or that exist. -->
    - **<Door>** – <its real options, or the tension in my notes>.
- **What will grow** – <modules, media kinds, categories…>. Don't shape shared concepts around <what's known today>.
- **Ideas in my notes** (<examples>) – sort them with me into first version / later / incubation. Specify only what the first milestones need.
- Answer in the language of my last message.

Stop interviewing when both levels have the depth set in _Scope_ and _Your Role_. Then tell me which questions remain open and why they can wait.


## Writing

Where: **`<repo>/docs/kickoff/`**, structured like this:

- **Folders & files** – kebab-case, full words (`first-version/`, not `v1/`). The home page is `README.md` (never `index.md`). A section is a sub-folder with its own `README.md` as main page.
- **Titles** – a page in a section has the h1 `{Section}: {Page}` (ex: `First Version: Catalog`); a section's `README.md` is just `{Section}`.
- **Reading map** – the home page has a `| Page | Answers |` table in reading order, one question line per page. Pages in a section go right under it, as `└ [{Page}]({section}/{page}.md)` (there's no `{Section}: ` prefix in these links).
- **`_toc.txt`** – the reading map as a plain list, for script processing (ex: merging the pages into one PDF): every page in reading-map order, `README.md` first, one path per line, relative to `docs/kickoff/` (ex: `vision/horizons.md`). Nothing else – no `_` files. Updated with the reading map.
- **Navigation bar** – the same line at the top of every page and again at the bottom, after a `---`. Ex, on a section's first page after its `README.md`: `[↑ Home](../README.md)&emsp;·&emsp;[← {Section}](README.md)&emsp;·&emsp;[{Section}: {Next Page} →](next-page.md)`.
    - Separator: `&emsp;·&emsp;` – a middle dot between two em spaces.
    - `↑ Home` always goes to the root `README.md` (`../README.md` from a section); the home page itself only has `[{First page} →](…)`.
    - `←` / `→` follow the reading map and are labeled with the target's h1: `[Vision →](vision/README.md)`, `[← First Version: CLI](../first-version/cli.md)`, `[Vision: Horizons →](horizons.md)`.
    - No `←` when the previous page is the home page; no `→` on the last page.
- **Legend** – the home page ends with a `## Legend` section holding this table, copied as is. Use no other marks.

    | Mark | Name | Meaning |
    | --- | --- | --- |
    | 🔀 `D001` | Decision | A significant choice: context, options, decision. AI's, from USER's notes and the interview; it stands until a 🤠 says otherwise. Numbered across the project, defined on the page it belongs to, listed in `decisions.md`. |
    | ⛔️ | One-way door | Expensive to undo; written with its cheap exit. Everything else is a two-way door: decide fast, fix later. |
    | 🧪 `S01` | Spike | An assumption to verify with a quick experiment before building on it. Numbered across the project, defined on the page it unblocks, listed in `roadmap.md`. |
    | 🧐 `AC-{CODE}-01` | Acceptance criterion | A testable "given … when … then …" statement – what the implementer checks against. ID: a short page code and a number (ex: `AC-ARCHI-03`). |
    | ❓ `Q001` | Open question | Something not known or not decided yet, said as such. Numbered across the project, defined on the page it belongs to, listed in `open-questions.md`. Removed once settled: the decision or the page is the answer. |
    | 🏁 `M01` | Milestone | A usable outcome, not a task list. Defined in `roadmap.md`, with the 🧪 it waits on. |
    | 🤠 | USER | Review feedback. Removed once applied: the page itself is the answer. |
    | 🪤 | Trap | Flagged by USER: too specific or short-sighted. Handled like 🤠. |
    | 🧞‍♂️ | AI | A proposal waiting for a yes/no, or a reply to 🤠 / 🪤 where a point stays open. |

- **Decisions** – in a quote block, like this:

    ```markdown
    > 🔀 ⛔️ **D{NNN} – {The decision, stated in a few words.}**
    > - _Context:_ {the problem, and what USER's notes, the code or other projects say}.
    > - _Options:_
    >     - (a) **{Option}** – {for}; but {against}.
    >     - (b) **{Option}** – {for}; but {against}.
    > - _Interview:_ {what USER said that led to the decision}.
    > - _Decision:_ (a). {Why, in a sentence or two.}
    > - _Cheap exit:_ {how to walk it back}.
    ```

    - The title states the decision, so that `decisions.md` reads as a summary.
    - ⛔️ and _Cheap exit:_ only on one-way doors. _Interview:_ only when USER's words drove the decision. An option needs no "for / but" when its name says it all.
    - Extra bullets when useful, same form: _Cost accepted:_, _First candidate:_, _Never built here:_…
    - The 🧪 or ❓ a decision depends on goes right after it, in the same quote.

**Vision pages** stay high-level: purpose, <stakeholders,> the parts and how they relate (a diagram helps), principles, relation to other projects, horizons (now / next / later). No acceptance criteria.

**First-version pages** cover, as relevant:

- **Purpose** – what it lets USER do, in 2–3 lines. What it can do, not only what USER plans to do with it.
- **Behavior** – <commands / screens / flows>, inputs, outputs, what happens on <rerun, crash, offline, missing data/drive, partial failure…>.
- **Data model & storage** – <entities, where data lives, identifiers>.
- **Acceptance criteria** – 🧐, for everything the implementer must check.
- **Out of scope** – explicitly. Ideas for later go to the roadmap.

Likely spikes here: <the project's assumptions worth a quick experiment, if any>.

End with three root pages:

- `roadmap.md` – the 🏁 milestones (ex: "<concrete outcome>"); then _Later_ (ideas parked for after the first version) and _Incubation_ (ideas that may resurface, or not).
- `decisions.md` – every 🔀, one line each: ID, ⛔️ if any, title, link to where it's defined.
- `open-questions.md` – every ❓ still open, one line each: ID, question, link to where it's defined.

Writing rules:

- People are named: USER and AI (or 🤠 and 🧞‍♂️) – never I, me, my or you.
- DRY: reference where something is defined; never copy it into several pages.
- Simplify in context unless it could confuse.
- En dash ` – ` in prose, Title Case headings, `_italic_` (not `*italic*`), 4-space indent for nested lists, TSV never CSV.


## Rules for This Session

- No code, no commits, no installs, no changes outside `docs/kickoff/`. If a quick experiment would settle a question, propose the exact command and let me run it.
- Work in these steps, pausing after each for my go-ahead (going back to an earlier one is fine):
    1. read & summarize
    2. vision interview
    3. first-version interview
    4. outline (the pages and what each answers)
    5. write
    6. self-review (contradictions, 🪤 traps, unmarked open questions, anything that breaks the _Writing_ rules, <project-specific risks> – then report them)
    7. my review (I add 🤠 and 🪤; you handle them as the legend says, then self-review again).
