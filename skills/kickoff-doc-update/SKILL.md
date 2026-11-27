---
name: kickoff-doc-update
description: Brings a project's kickoff docs (`{repo}/docs/kickoff/`) up to the current version of the doc conventions of the kickoff-doc-prompt skill – the form only, never the content – and refreshes their references to other projects. Use when those docs follow an older version, or none written down, or when a project they reference has changed. Not for writing the kickoff prompt (that's kickoff-doc-prompt), nor for writing or changing what the docs say.
disable-model-invocation: true
---

# Kickoff Doc Update

Brings `<repo>/docs/kickoff/` to the current version of the doc conventions. It changes **the form only, never the content**: no decision, question, criterion or fact is added, removed or reworded beyond what the new form requires.

You migrate, you don't review. A gap or a mistake in the content is reported, never fixed.


## Sources of Truth

The conventions belong to the `kickoff-doc-prompt` skill. This skill holds no copy of them, and nothing shared lives here.

- `kickoff-doc-prompt/conventions.md` – the current conventions, versioned by its `Version:` line.
- `kickoff-doc-prompt/check.py` – checks a docs folder against them: `python3 check.py <repo>/docs/kickoff`.
- `kickoff-doc-prompt/template.md` – the current prompt, for step 6 only.
- `<repo>/docs/kickoff/_conventions.md` – the version the docs follow, when they have one.
- `<repo>/docs/kickoff/external-references.md` – the other projects the docs reference, where their docs are, and what each referenced ID is.
- This file – the workflow.

**Finding `kickoff-doc-prompt`:** the first of these that holds `conventions.md`. Say which one in the report.

1. **A local clone** – `../kickoff-doc-prompt/`, the sibling folder of this skill.
2. **An installed copy** – under `~/Library/Application Support/Claude/`, a `…/skills/kickoff-doc-prompt/` folder: each installed skill sits in its own `plugin_<id>/skills/<skill>/`. Several: take the highest `Version:`.
3. **The official current version** – `https://raw.githubusercontent.com/ppo/claude/main/skills/kickoff-doc-prompt/`, which needs the network. Download `conventions.md`, `check.py` and `template.md` into a temp folder, and run `python3 -I <temp>/check.py`.

None works: stop and ask the user.


## Order and Reruns

What others rest on goes first, and a rerun redoes only what depends on something that changed.

- **Referenced projects first.** Docs that reference another project read its paths and titles. If that project's docs are behind (an older `_conventions.md`, or none), the user chooses:
    - Update that project first – this skill, run there – then come back.
    - Go on now with its current paths and titles, and rerun here once it's updated.
- **A rerun at the same version** only refreshes `external-references.md` – docs folders, paths, titles – from each referenced project. An ID that is gone there, or that now means something else, is reported, never removed or reworded: it's content.
- **Several projects to update:** start with those that reference no other one, then follow the references.


## Workflow

1. **Locate.** Confirm the repo path; if the user gave none, ask. Read every page in `_toc.txt` order, `_toc.txt` itself, `_kickoff-doc-prompt.md` and `_conventions.md` if any.
    - _No `_toc.txt`_ (docs older than it): write it first, from the pages as they are – in the reading map's order, or the home page's links when it has none, `README.md` first. `check.py` needs it. Ask when the order isn't clear.
2. **Find the versions.**
    - _This project's:_ `_conventions.md`'s `Version:`. A copy can lie – put there by hand, never applied: if `check.py` reports many problems at that version, or the status note never mentions it, ask before trusting it. Docs older than versioning have none. Their conventions are then the `## Writing` section of the prompt, or nothing written down at all, in which case the pages themselves show the old forms.
    - _Referenced projects':_ every other project the pages name – from `external-references.md`, or else from the pages and `_kickoff-doc-prompt.md`'s reading list. For each: its docs folder (`~` for the home folder), and the version they follow.
3. **List the changes.** If the old version is the current one, refresh the external references (see _Order and Reruns_) and stop. Otherwise, compare the old conventions with the current ones, section by section. Running `check.py` on the unchanged docs maps where each change bites. List each rule that changed: old form → new form, and the pages it affects. Leave out wording changes that ask nothing of the pages.
4. **Sort them with the user**, before any edit, in one table (`| Rule | Old → New | Pages | Kind |`):
    - _Form_ – applied: renames, IDs, navigation, index tables, legend, decision layout, typography…
    - _Needs content_ – a new required section or field that the pages can't fill from what they already say. Never invent it: list it.
    - _Doubtful_ – a change that could alter meaning (ex: a sentence to reword for the voice rule, a spike definition to move to another page, a sentence that states an old convention). Ask, with `AskUserQuestion`, your recommendation first.

    Then, separately: each referenced project that is behind, and the choice in _Order and Reruns_.
5. **Apply** the form changes, page by page, in reading order:
    - IDs stay stable. Where the new form renumbers them, map old → new in one table and update every reference.
    - A renamed file or folder: update every link, `_toc.txt`, the reading map and the navigation bars. A broken link to a `_` file means it was renamed by hand: point it to the current name.
    - **A section without its `README.md`:** create it. A short page: what the section covers, in a sentence or two taken from its pages, then its pages in a `| Page | Answers |` table, in reading order – the section's own reading map. It goes into the home page's reading map, `_toc.txt` and the navigation bars, right before the section's pages. It's the one page this skill writes: nothing in it that the pages don't already say.
    - Index tables (`decisions.md`, `open-questions.md`, the spikes in `roadmap.md`) follow their definitions: same titles, same marks, links to the defining section. A title copies its definition's even when the old index summed it up better: an index is a reference, the details are in the pages. Nothing to report.
    - **Another project's IDs** become `↗️ {Project} {ID}`, ranges and lists included. Each ID gets its row in `external-references.md`, with the path and title read in that project's docs – read only, never fixed. A title found nowhere: _Needs content_.
    - **Decision states**, in docs older than them. A state says who decided, which is content: propose them all in one table (`| Decision | State | Why |`), and apply what the user confirms or corrects.
        - A decision with a 🧞‍♂️ proposal bullet: ℹ️, the bullet becoming `> - ℹ️ …`, when the pages apply the proposal; else ❗️.
        - A proposal outside any decision (once in `open-questions.md`): a new decision, ℹ️ when the pages apply it, ❗️ when it's a choice still to make; anything else, a ❓. New IDs follow the highest.
        - Any other decision: ✅ when USER's words settled it (an _Interview:_ bullet, USER's notes, an applied 🤠); ℹ️ when AI chose alone.
    - **Voice:** a pronoun for an actor – who does what – becomes USER or AI, when the sentence means the same. Anything more is _Doubtful_. Quotes, UI labels, the app's own content and the I / you of 🤠 / 🧞‍♂️ discussions stay as written.
6. **Update the prompt** `_kickoff-doc-prompt.md` to the current `template.md` only on the user's yes: the prompt records how the docs were made. Keep everything project-specific it says, and move its old conventions part into the template's `## Writing` form.
7. **Record it.** In the home page's status note, add a last paragraph: `**Updated on {date}** to conventions {version}: {the main changes, in a few words}. The content is unchanged.` If the last paragraph is already of today, replace it with one saying what both changed. Use the date format the note already uses. Then replace `_conventions.md` with the current `conventions.md`, as is: `cp -a <kickoff-doc-prompt>/conventions.md <repo>/docs/kickoff/_conventions.md`, never retyped.
8. **Check.** Run `check.py` and fix every problem. Look at each warning: fix it, or keep it on purpose as a deviation. Then re-read for what the script can't see. Review `git -C <repo> diff --word-diff -- docs/kickoff` and make sure every changed word comes from a rule in the change list.
9. **Report:** what changed, by rule; the ID map, if any; what was left for the user (_Needs content_, _Doubtful_); the referenced projects still behind, and when a rerun is due; and each deliberate deviation from the conventions, with why. Deviations are input for the next version. No commits: they're the user's.


## Quality Checks

- Edits only inside `<repo>/docs/kickoff/`: `git status` shows nothing else, here and in every referenced project.
- `check.py` reports no problem. Each warning is fixed or reported as a deviation.
- The word diff is form only. No ID is lost, reused or pointing elsewhere. Every ❓ and 🧪 that was there is still there, and every 🧞‍♂️ proposal is now an ℹ️, a ❗️ or a ❓.
- `_conventions.md` is byte-identical to the `conventions.md` used, and the status note names its version.
