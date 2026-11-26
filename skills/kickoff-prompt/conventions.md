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
    - A status note in a quote: who wrote the docs, when, from what, and whether they describe what is built or what is designed. One `**Updated on {date}**` paragraph per later change, saying what changed. A second change on the same day replaces that day's paragraph, which then says what both changed.
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
| 🔀 `D001` | Decision | A choice, small or large, with the fields it needs. Always followed by its state: ❗️, ℹ️ or ✅. Numbered across the project, defined on the page it belongs to, listed in `decisions.md`. |
| ❗️ | To decide | A decision stated, not made yet: its options, and AI's recommendation if any. |
| ℹ️ | FYI | Decided and applied by AI alone, beyond what USER said or wrote. It stands unless a 🤠 says otherwise. On a bullet: the part AI decided alone. |
| ✅ | Done | Settled by USER's words – notes, interview, a 🤠 – or agreed by USER after an ℹ️. |
| ⛔️ | One-way door | Expensive to undo; written with its cheap exit. Everything else is a two-way door: decide fast, fix later. |
| 🧪 `S01` | Spike | An assumption to verify with a quick experiment before building on it. Numbered across the project, defined where it is first needed, listed in `roadmap.md`. |
| 🧐 `AC-{CODE}-01` | Acceptance criterion | A testable "given … when … then …" statement – what the implementer checks against. ID: a short page code and a number (ex: `AC-ARCHI-03`). |
| ❓ `Q001` | Open question | Anything to find out that isn't a decision: a fact not known yet, a request for information or direction. Numbered across the project, defined on the page it belongs to, listed in `open-questions.md`. Removed once settled: the decision or the page is the answer. |
| 🏁 `M01` | Milestone | A usable outcome, not a task list. Defined in `roadmap.md`, with the 🧪 it waits on. |
| ↗️ | External reference | Another project's item: `↗️ {Project} {ID}`. A bare ID is always this project's. Listed in `external-references.md`. |
| 🤠 / 🧞‍♂️ | USER / AI | A discussion on the page, in blocks: each one starts with the mark of who's talking. Once the discussion is closed, AI removes it – the page itself is the answer. |
| 🤠 | USER | Feedback: a comment on anything. On a decision, it acts: USER decides (a ❗️ – what's to be done), objects or redirects, usually with comments. |
| 🧞‍♂️ | AI | Usually answering a 🤠, when the subject can't yet be applied or closed. |
| 🪤 | Trap | An inline flag, anywhere: a wrong call, a mistake in judgment, short-sighted, too specific. Temporary: it must be resolved. Usually in the text after a 🤠 / 🧞‍♂️. |


## Marks and IDs

IDs are numbered across the project, never reused, never renumbered: a removed ID leaves a gap.

### Decisions

In a quote block:

```markdown
> 🔀✅⛔️ **D{NNN} – {The decision, stated in a few words.}**
> - _Context:_ {the problem, and what USER's notes, the code or other projects say}.
> - _Options:_
>     - (a) **{Option}** – {for}; but {against}.
>     - (b) **{Option}** – {for}; but {against}.
> - _Interview:_ {what USER said that led to the decision}.
> - _Decision:_ (a). {Why, in a sentence or two.}
> - _Cheap exit:_ {how to walk it back}.
```

- **Marks:** 🔀, its state, then ⛔️ on a one-way door – with no space between them (`🔀❗️⛔️`), so that each combination can be searched for.
- **Small or large:** the title line alone can be enough. Add the fields that help.
- The title states the decision, so that `decisions.md` reads as a summary. Still ❗️: it states what is to decide.
- **States:**
    - ❗️ _To decide_ – no `_Decision:_` yet; `_Recommendation:_ (a). {Why.}` when AI has one. What AI has already decided and applied goes on its own bullets: `> - ℹ️ {What AI decided}.`
    - ℹ️ _FYI_ – AI decided and applied it, beyond what USER said or wrote – quick calls on minor choices included. When only part of it is AI's, that part goes on an ℹ️ bullet.
    - ✅ _Done_ – USER's words settled it, or USER agreed to the ℹ️. No ℹ️ bullet left.

    A decision takes its least settled state: a part still open makes it ❗️; else a part AI decided alone makes it ℹ️.
- **Changing a decision:** USER decides, objects or redirects with a 🤠, right after the decision; USER never edits a decision block directly. AI applies the 🤠 – options, decision, state – and removes it. A 🤠 that agrees turns ℹ️ into ✅.
- ⛔️ and _Cheap exit:_ only on one-way doors – a ❗️⛔️ gets its exit once decided. _Interview:_ only when USER's words drove the decision. An option needs no "for / but" when its name says it all.
- A one-way door with several risks gets one sub-bullet per risk, each `{risk} → {exit}`:

    ```markdown
    > - _Cheap exit:_
    >     - {Risk} → {how to walk it back}.
    >     - {Risk} → {how to walk it back}.
    ```

- A risk with no cheap exit says so, with what limits the damage: `> - _No cheap exit:_ {what can't be undone}. Hence: {what makes it unlikely or small}.`
- Extra bullets when useful, same form: _Cost accepted:_, _First candidate:_, _Never built here:_…
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

Usually in a page's `## Open Questions` section, or right after the decision it bears on. A choice to make is not a question: it's a 🔀❗️ decision.

### Milestones

In `roadmap.md`, one heading each: `### 🏁 M{NN} – {Outcome, in Title Case}`, then what changes for USER, what it retires, the 🧪 it waits on, and "It is reached when" – the pages whose acceptance criteria all pass.

### External References

`↗️ {Project} {ID}` – ex: `↗️ Andy CLI D003`, a range `↗️ Andy CLI D008–D010`, a list `↗️ Andy CLI D014, D015`. Never a link: the other project's docs can move, renumber or disappear. Every ID gets a row in `external-references.md`, which says what it is.


## Pages

**Vision pages** stay high-level: purpose, stakeholders if any, the parts and how they relate (a diagram helps), principles, relation to other projects, horizons (now / next / later). No acceptance criteria. When the docs depart from USER's earlier notes or attempts, an optional `## Departures From USER's Earlier Notes` table says where: `| Decision | Earlier | Now |`.

**First-version pages** cover, as relevant:

- **Purpose** – what it lets USER do, in 2–3 lines. What it can do, not only what USER plans to do with it.
- **Behavior** – inputs, outputs, and what happens on the failures that matter to this project.
- **Data model & storage** – the entities needed now, where data lives, identifiers.
- **Acceptance criteria** – 🧐, for everything the implementer must check.
- **Out of scope** – explicitly. Ideas for later go to the roadmap.

**Four root pages** end the reading map:

- `roadmap.md` – the 🏁 milestones; then `## Later` (ideas parked for after the first version) and `## Incubation` (ideas that may resurface, or not).
- `decisions.md` – every 🔀:

    ```markdown
    | ID | Decision | Page |
    | --- | --- | --- |
    | 🔀✅⛔️ D001 | {Title of the decision.} | [{Page}]({path}#{section-anchor}) |
    ```

    The marks are those of the decision, as on its page: `🔀❗️` finds everything still to decide.

- `open-questions.md` – every ❓ still open, in the same table form (`| ID | Question | Page |`, the ID bare).
- `external-references.md` – every ↗️, one row per ID (a range or a list gives one row each). Above the table, one line per project with its docs folder, `~` for the home folder. Page paths are relative to that folder, and titles are as that project writes them. A project whose docs move or renumber: update the line and the rows, not the pages.

    ```markdown
    - Andy CLI – `~/dev/andy/andy-cli/docs/kickoff/`

    | Project | Reference | Page | Title |
    | --- | --- | --- | --- |
    | Andy CLI | 🔀 D003 | `first-version/storage.md` | {Title, as that project writes it.} |
    ```

Index lines of this project's items link to the section where the item is defined, not just to the page.


## Writing Rules

- **Actors are named:** who does what is USER or AI (or 🤠 and 🧞‍♂️) – never I, me, my or you, and no pronoun for either: repeat "USER" or "AI", even when it reads stiffly. Not about actors, so as written: quotes, UI labels, and any text that is part of the app's content (ex: a column `My ID`).
- **Another project's IDs** – always `↗️ {Project} {ID}` ([External References](#external-references)).
- **DRY:** reference where something is defined; never copy it into several pages.
- **Simplify in context** unless it could confuse.
- **Typography:** en dash ` – ` in prose, Title Case headings, `_italic_` (not `*italic*`), 4-space indent for nested lists, TSV never CSV.
