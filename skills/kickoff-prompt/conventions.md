# Kickoff Docs – Conventions

Version: 261126

How the docs in `<repo>/docs/kickoff/` are written, for any session that writes or edits them. Each project keeps a copy as `docs/kickoff/_conventions.md`: it records the version the docs follow. The copy is never edited by hand. It is replaced as a whole when the docs move to a newer version.

These are defaults. When a page needs something they don't cover, or a rule fits badly, do what serves the reader, then list the deviation in the self-review. Deviations are how these conventions improve.

`{…}` is a placeholder to fill.


## Structure

- **Folders & files** – kebab-case, full words (`first-version/`, not `v1/`). The home page is `README.md` (never `index.md`). A section is a sub-folder with its own `README.md` as main page.
- **Titles** – a page in a section has the h1 `{Section}: {Page}` (ex: `First Version: Catalog`); a section's `README.md` is just `{Section}`.
- **Home page** – `README.md`, in this order:
    - What the project is, and the depths these pages cover.
    - A status note in a quote: who wrote the docs, when, from what, and whether they describe what is built or what is designed. One `**Updated on {date}**` paragraph per later change, saying what changed.
    - The sources, and a link to [`_kickoff-prompt.md`](_kickoff-prompt.md).
    - `## Reading Map` – a `| Page | Answers |` table in reading order, one question line per page. Pages in a section go right under it, as `└ [{Page}]({section}/{page}.md)` (no `{Section}: ` prefix in these links).
    - `## Legend` – the table below, copied as is.
- **`_toc.txt`** – the reading map as a plain list, for script processing (ex: merging the pages into one PDF): every page in reading-map order, `README.md` first, one path per line, relative to `docs/kickoff/` (ex: `vision/horizons.md`). Nothing else – no `_` files. Updated with the reading map.
- **`_` files** – `_kickoff-prompt.md`, `_conventions.md`: about the docs, not part of them. Not in the reading map, `_toc.txt` or the navigation.
- **Navigation bar** – the same line at the top of every page and again at the bottom, after a `---`. Ex, on a section's first page after its `README.md`: `[↑ Home](../README.md)&emsp;·&emsp;[← {Section}](README.md)&emsp;·&emsp;[{Section}: {Next Page} →](next-page.md)`.
    - Separator: `&emsp;·&emsp;` – a middle dot between two em spaces.
    - `↑ Home` always goes to the root `README.md` (`../README.md` from a section); the home page itself only has `[{First page} →](…)`.
    - `←` / `→` follow the reading map and are labeled with the target's h1: `[Vision →](vision/README.md)`, `[← First Version: CLI](../first-version/cli.md)`, `[Vision: Horizons →](horizons.md)`.
    - No `←` when the previous page is the home page; no `→` on the last page.


## Legend

Copied as is at the end of the home page. Use no other marks.

| Mark | Name | Meaning |
| --- | --- | --- |
| 🔀 `D001` | Decision | A significant choice: context, options, decision. AI's, from USER's notes and the interview; it stands until a 🤠 says otherwise. Numbered across the project, defined on the page it belongs to, listed in `decisions.md`. |
| ⛔️ | One-way door | Expensive to undo; written with its cheap exit. Everything else is a two-way door: decide fast, fix later. |
| 🧪 `S01` | Spike | An assumption to verify with a quick experiment before building on it. Numbered across the project, defined where it is first needed, listed in `roadmap.md`. |
| 🧐 `AC-{CODE}-01` | Acceptance criterion | A testable "given … when … then …" statement – what the implementer checks against. ID: a short page code and a number (ex: `AC-ARCHI-03`). |
| ❓ `Q001` | Open question | Something not known or not decided yet, said as such. Numbered across the project, defined on the page it belongs to, listed in `open-questions.md`. Removed once settled: the decision or the page is the answer. |
| 🏁 `M01` | Milestone | A usable outcome, not a task list. Defined in `roadmap.md`, with the 🧪 it waits on. |
| 🤠 | USER | Review feedback. Removed once applied: the page itself is the answer. |
| 🪤 | Trap | Flagged by USER: too specific or short-sighted. Handled like 🤠. |
| 🧞‍♂️ | AI | A proposal waiting for a yes/no, or a reply to 🤠 / 🪤 where a point stays open. Proposals are listed in `open-questions.md`. |


## Marks and IDs

IDs are numbered across the project, never reused, never renumbered: a removed ID leaves a gap.

### Decisions

In a quote block:

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
- A one-way door with several risks gets one sub-bullet per risk, each `{risk} → {exit}`:

    ```markdown
    > - _Cheap exit:_
    >     - {Risk} → {how to walk it back}.
    >     - {Risk} → {how to walk it back}.
    ```

- A risk with no cheap exit says so, with what limits the damage: `> - _No cheap exit:_ {what can't be undone}. Hence: {what makes it unlikely or small}.`
- Extra bullets when useful, same form: _Cost accepted:_, _First candidate:_, _Never built here:_…
- A 🧞‍♂️ proposal inside a decision goes on its own bullet: `> - 🧞‍♂️ {the proposal, beyond what USER said}.`
- The 🧪 or ❓ a decision depends on goes right after it, in the same quote.

### Spikes

`🧪 **S{NN} – {What to check}.** {Why it matters, then the exact commands USER runs and what each result decides.}`

Defined where it is first needed: on the first page, in reading order, that it unblocks or relates to – a vision page if it unblocks a later horizon. Another page that needs it points to it; a page that holds a part of it starts with `🧪 **Part of S{NN} – {What to check}.**`

### Acceptance Criteria

`- 🧐 **AC-{CODE}-{NN}** – Given {state}, when {action}, then {result}.`

- `{CODE}` is short and unique per page (ex: `CAT` for Catalog). "When" can be left out when "given" is the action.
- In an `## Acceptance Criteria` section, grouped by the milestone that needs them: a `**🏁 M{NN}**` line before each group, or one line `All 🏁 M{NN}.` when the whole page belongs to one. The roadmap's "It is reached when" relies on it.

### Open Questions

`❓ **Q{NNN}** – {The question.} {Why it can wait, or what settles it.}`

Usually in a page's `## Open Questions` section, or right after the decision it bears on.

### Milestones

In `roadmap.md`, one heading each: `### 🏁 M{NN} – {Outcome, in Title Case}`, then what changes for USER, what it retires, the 🧪 it waits on, and "It is reached when" – the pages whose acceptance criteria all pass.


## Pages

**Vision pages** stay high-level: purpose, stakeholders if any, the parts and how they relate (a diagram helps), principles, relation to other projects, horizons (now / next / later). No acceptance criteria. When the docs depart from USER's earlier notes or attempts, an optional `## Departures From USER's Earlier Notes` table says where: `| Decision | Earlier | Now |`.

**First-version pages** cover, as relevant:

- **Purpose** – what it lets USER do, in 2–3 lines. What it can do, not only what USER plans to do with it.
- **Behavior** – inputs, outputs, and what happens on the failures that matter to this project.
- **Data model & storage** – the entities needed now, where data lives, identifiers.
- **Acceptance criteria** – 🧐, for everything the implementer must check.
- **Out of scope** – explicitly. Ideas for later go to the roadmap.

**Three root pages** end the reading map:

- `roadmap.md` – the 🏁 milestones; then `## Later` (ideas parked for after the first version) and `## Incubation` (ideas that may resurface, or not).
- `decisions.md` – every 🔀:

    ```markdown
    | ID | Decision | Page |
    | --- | --- | --- |
    | D001 ⛔️ | {Title of the decision.} | [{Page}]({path}#{section-anchor}) |
    ```

- `open-questions.md` – every ❓ still open, in the same table form (`| ID | Question | Page |`). Then `## Proposals Waiting for a Yes/No`: every 🧞‍♂️ proposal still open, one line each – `- {The proposal} – [{Page}]({path}#{section-anchor}) D{NNN}`, the decision only when there is one.

Index lines link to the section where the item is defined, not just to the page.


## Writing Rules

- **People are named:** USER and AI (or 🤠 and 🧞‍♂️) – never I, me, my or you, and no pronoun for either: repeat "USER" or "AI", even when it reads stiffly. Kept as written, in quotes or code: quotes of USER's notes, UI labels (ex: `My ID`), titles of works.
- **Another project's IDs** are written in full, so they stay understandable if that project renumbers, moves or disappears: `{Project} {ID} ({path of its page, relative to that project's docs folder} – {title})`, never as a link. Ex: `Andy CLI D003 (first-version/storage.md – A location = a medium root + a logical relative path)`. Once a page has given the full form, later mentions on that page can be `Andy CLI D003`. A bare `D003` is always this project's.
- **DRY:** reference where something is defined; never copy it into several pages.
- **Simplify in context** unless it could confuse.
- **Typography:** en dash ` – ` in prose, Title Case headings, `_italic_` (not `*italic*`), 4-space indent for nested lists, TSV never CSV.
