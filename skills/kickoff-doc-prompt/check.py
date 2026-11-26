#!/usr/bin/env python3
"""Check a kickoff docs folder against conventions.md.

    python3 check.py <repo>/docs/kickoff [--conventions <path>]

`--conventions` defaults to the conventions.md next to this script.
Problems break a rule. Warnings come from heuristics: look at each one, and fix it or keep it on purpose.
Exit code 1 when there is a problem. Python standard library only.
"""
import argparse
import bisect
import re
import sys
from collections import defaultdict
from pathlib import Path

ID = r"(?:[DQ]\d{3}|[SM]\d{2})"
ID_RE = re.compile(rf"\b({ID})\b")
XID = rf"(?:{ID}|AC-[A-Z]+-\d{{2}})"
# `↗️ {Project} {ID}`, a range `D008–D010` or a list `D014, D015`.
XREF = re.compile(rf"↗️? ([A-Z][\w.+-]*(?: [A-Z][\w.+-]*)*?) ({XID}(?:(?:–|, | and ){XID})*)\b")
SEP = "&emsp;·&emsp;"
INLINE_CODE = re.compile(r"`[^`]*`")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
SMALL_WORDS = set("a an the and or nor but for of in on at to by from with as vs via per into onto over".split())
# Leading words that make a capitalized run look like a project name when it isn't one.
NOT_PROJECT = set(
    "A An The And Or But See After Before Until Since With Without By In On At To From For Like As Also Then "
    "Only Both Each Every All Its Their Spike Spikes Decision Decisions Question Questions Milestone Milestones "
    "Proposal Proposals Part".split()
)
MARKS = {"🔀", "❗", "ℹ", "✅", "⛔", "🧪", "🧐", "❓", "🏁", "↗", "🤠", "🪤", "🧞", "♂"}
# `🔀❗️⛔️ **D001 – …**`: the state (❗️ to decide, ℹ️ FYI, ✅ done), then ⛔️, with no space between the marks.
DECISION = re.compile(r"🔀(?P<sp1> *)(?P<state>❗\ufe0f?|ℹ\ufe0f?|✅)?(?P<sp2> *)(?P<door>⛔\ufe0f?)? \*\*(?P<id>D\d{3}) – (?P<title>.+?)\*\*")
STATES = {"❗": "❗️", "ℹ": "ℹ️", "✅": "✅"}
INFO_BULLET = re.compile(r">\s*- ℹ")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿⏩-⏺]")


def slugify(text):
    """GitHub's anchor for a heading: no duplicate handling here."""
    text = LINK.sub(r"\1", text)
    text = re.sub(r"[*`]|(?<!\w)_|_(?!\w)", "", text)
    text = re.sub(r"[^\w\- ]", "", text.lower())
    return text.replace(" ", "-")


class Page:
    def __init__(self, root, rel):
        self.rel = rel
        self.dir = str(Path(rel).parent) if "/" in rel else ""
        self.lines = (root / rel).read_text(encoding="utf-8").split("\n")
        self.prose = []  # lines with fenced code blanked and inline code removed
        self.headings = []  # (line index, level, text, slug)
        fenced, seen = False, defaultdict(int)
        for i, line in enumerate(self.lines):
            if re.sub(r"^[>\s]*", "", line).startswith("```"):
                fenced = not fenced
                self.prose.append("")
                continue
            self.prose.append("" if fenced else INLINE_CODE.sub("", line))
            m = None if fenced else re.match(r"(#{1,6}) (.+)", line)
            if m:
                base = slugify(m.group(2).strip())
                slug = base if not seen[base] else f"{base}-{seen[base]}"
                seen[base] += 1
                self.headings.append((i, len(m.group(1)), m.group(2).strip(), slug))
        self.h1 = next((h[2] for h in self.headings if h[1] == 1), None)
        self.slugs = {h[3] for h in self.headings}
        self.heading_lines = [h[0] for h in self.headings]

    def section_at(self, i):
        """Slug of the nearest heading at or above line i."""
        k = bisect.bisect_right(self.heading_lines, i) - 1
        return self.headings[k][3] if k >= 0 else ""

    def section_lines(self, title):
        """Indexes of the lines under the `## {title}` heading, up to the next heading of level ≤ 2."""
        for n, (i, level, text, _) in enumerate(self.headings):
            if level == 2 and text == title:
                end = next((h[0] for h in self.headings[n + 1:] if h[1] <= 2), len(self.lines))
                return range(i + 1, end)
        return None


class Report:
    def __init__(self):
        self.items = defaultdict(list)

    def problem(self, where, msg):
        self.items[where].append(("problem", msg))

    def warn(self, where, msg):
        self.items[where].append(("warning", msg))

    def count(self, kind):
        return sum(k == kind for items in self.items.values() for k, _ in items)


def rel_link(src_dir, target):
    return str(Path(*([".."] * len(Path(src_dir).parts)), target)) if src_dir else target


def is_underscore(rel):
    return any(part.startswith("_") for part in Path(rel).parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("docs", help="the <repo>/docs/kickoff folder")
    ap.add_argument("--conventions", default=str(Path(__file__).resolve().parent / "conventions.md"))
    args = ap.parse_args()
    root = Path(args.docs).resolve()
    r = Report()

    # --- Conventions and their copy ---------------------------------------------------------------
    conv_path = Path(args.conventions)
    conv = conv_path.read_text(encoding="utf-8") if conv_path.is_file() else None
    version = lambda text: (re.search(r"^Version: (\S+)", text, re.M) or [None, None])[1]
    if conv is None:
        r.warn("(setup)", f"no conventions at {conv_path}: legend and version not checked")
    copy = root / "_conventions.md"
    if not copy.is_file():
        r.problem("_conventions.md", "missing: the docs record no conventions version")
    elif conv is not None:
        old, new = version(copy.read_text(encoding="utf-8")), version(conv)
        if old != new:
            r.problem("_conventions.md", f"version {old}, current is {new}")
        elif copy.read_text(encoding="utf-8") != conv:
            r.problem("_conventions.md", f"differs from conventions.md {new}: it is never edited by hand")
    if not (root / "_kickoff-doc-prompt.md").is_file():
        r.warn("_kickoff-doc-prompt.md", "missing")

    # --- _toc.txt and the files ----------------------------------------------------------------------
    toc_file = root / "_toc.txt"
    if not toc_file.is_file():
        r.problem("_toc.txt", "missing")
        return finish(r)
    toc = [l.strip() for l in toc_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not toc or toc[0] != "README.md":
        r.problem("_toc.txt", "README.md must come first")
    for rel in toc:
        if is_underscore(rel):
            r.problem("_toc.txt", f"lists the `_` file {rel}")
        if not (root / rel).is_file():
            r.problem("_toc.txt", f"lists missing {rel}")
    toc = [rel for rel in toc if (root / rel).is_file() and not is_underscore(rel)]
    all_md = sorted(str(p.relative_to(root)) for p in root.rglob("*.md"))
    for rel in all_md:
        if not is_underscore(rel) and rel not in toc:
            r.problem(rel, "not in _toc.txt")
        parts = Path(rel).parts
        for part in parts[:-1] + (Path(rel).stem,):
            if part != "README" and not part.startswith("_") and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", part):
                r.problem(rel, f"`{part}` is not kebab-case")
        if parts[-1] == "index.md":
            r.problem(rel, "the main page is README.md, never index.md")

    pages = {rel: Page(root, rel) for rel in toc}
    order = {rel: n for n, rel in enumerate(toc)}
    for p in pages.values():
        if p.h1 is None:
            r.problem(p.rel, "no h1")
    home = pages.get("README.md")
    own_name = home.h1 if home else None

    check_titles(pages, r)
    check_nav(toc, pages, r)
    if home:
        check_home(home, toc, pages, conv, r)
    check_links(root, pages, r)
    check_ids(pages, order, own_name, r)
    check_writing(pages, r)
    return finish(r, toc)


def check_titles(pages, r):
    for p in pages.values():
        if p.dir and not p.rel.endswith("README.md") and p.h1:
            section = pages.get(f"{p.dir}/README.md")
            if section and section.h1 and not p.h1.startswith(f"{section.h1}: "):
                r.problem(p.rel, f"h1 `{p.h1}` should be `{section.h1}: …`")


def check_nav(toc, pages, r):
    for n, rel in enumerate(toc):
        p = pages[rel]
        parts = []
        if n > 0:
            parts.append(f"[↑ Home]({rel_link(p.dir, 'README.md')})")
        if n > 1:
            prev = toc[n - 1]
            parts.append(f"[← {pages[prev].h1}]({rel_link(p.dir, prev) if p.dir != pages[prev].dir else Path(prev).name})")
        if n < len(toc) - 1:
            nxt = toc[n + 1]
            parts.append(f"[{pages[nxt].h1} →]({rel_link(p.dir, nxt) if p.dir != pages[nxt].dir else Path(nxt).name})")
        expected = SEP.join(parts)
        lines = [l for l in p.lines]
        while lines and not lines[-1].strip():
            lines.pop()
        top, bottom = (lines[0], lines[-1]) if lines else ("", "")
        if top != expected:
            r.problem(rel, f"top navigation\n      got      {top}\n      expected {expected}")
        if bottom != expected:
            r.problem(rel, f"bottom navigation\n      got      {bottom}\n      expected {expected}")
        before = [l for l in lines[:-1] if l.strip()]
        if not before or before[-1] != "---":
            r.problem(rel, "no `---` before the bottom navigation")


def check_home(home, toc, pages, conv, r):
    heads = {h[2]: h[0] for h in home.headings if h[1] == 2}
    map_at, legend_at = heads.get("Reading Map"), heads.get("Legend")
    if map_at is None:
        r.problem("README.md", "no `## Reading Map`")
    if legend_at is None:
        r.problem("README.md", "no `## Legend`")
    elif max(heads.values()) != legend_at:
        r.problem("README.md", "`## Legend` must be the last section")
    first_map = map_at if map_at is not None else len(home.lines)
    if not any(l.startswith(">") for l in home.lines[:first_map]):
        r.problem("README.md", "no status note (a quote) before the reading map")
    if not any("](_kickoff-doc-prompt.md)" in l for l in home.lines[:first_map]):
        r.problem("README.md", "no link to _kickoff-doc-prompt.md before the reading map")

    rows = home.section_lines("Reading Map") or []
    listed = []
    for i in rows:
        m = re.match(r"\| (└ )?\[([^\]]+)\]\(([^)]+)\) \|", home.lines[i])
        if not m:
            continue
        sub, text, target = m.groups()
        listed.append(target)
        page = pages.get(target)
        if not page:
            continue
        if sub:
            if not page.dir or target.endswith("README.md"):
                r.problem("README.md", f"reading map: `└` on {target}, which is not a page in a section")
            if page.h1 and not page.h1.endswith(f": {text}"):
                r.warn("README.md", f"reading map: `{text}` doesn't match the h1 `{page.h1}`")
        else:
            if page.dir and not target.endswith("README.md"):
                r.problem("README.md", f"reading map: {target} is in a section, so its row starts with `└ `")
            if page.h1 and text != page.h1:
                r.warn("README.md", f"reading map: `{text}` doesn't match the h1 `{page.h1}`")
    if listed != toc[1:]:
        diff = next((n for n, (a, b) in enumerate(zip(listed, toc[1:])) if a != b), min(len(listed), len(toc) - 1))
        r.problem("README.md", f"reading map and _toc.txt differ from row {diff + 1} "
                               f"(map: {listed[diff] if diff < len(listed) else '–'}, toc: {toc[diff + 1] if diff + 1 < len(toc) else '–'})")

    if conv is not None and legend_at is not None:
        want = [l for l in section_text(conv, "Legend") if l.startswith("|")]
        got = [home.lines[i] for i in home.section_lines("Legend") if home.lines[i].startswith("|")]
        if got != want:
            bad = next((w for w, g in zip(want, got) if w != g), None) or f"{len(got)} rows instead of {len(want)}"
            r.problem("README.md", f"legend differs from conventions.md, first at: {bad[:90]}")


def section_text(text, title):
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith("## "):
            inside = line[3:].strip() == title
        elif inside:
            out.append(line)
    return out


def check_links(root, pages, r):
    for p in pages.values():
        for line in p.prose:
            for _, target in LINK.findall(line):
                if re.match(r"[a-z]+:", target):
                    continue
                f, _, anchor = target.partition("#")
                dest = (root / p.dir / f).resolve() if f else root / p.rel
                if root not in dest.parents and dest != root:
                    r.warn(p.rel, f"link leaves docs/kickoff: {target}")
                    continue
                if not dest.exists():
                    r.problem(p.rel, f"broken link {target}")
                    continue
                if anchor and dest.suffix == ".md":
                    rel = str(dest.relative_to(root))
                    target_page = pages.get(rel) or Page(root, rel)
                    if anchor not in target_page.slugs:
                        r.problem(p.rel, f"missing anchor {target}")


def check_ids(pages, order, own_name, r):
    defs = defaultdict(list)  # id → [(page, line index)]
    spike_parts = defaultdict(list)
    decisions = {}  # D → (page, line, title, one_way, quote lines, state)
    quoted = defaultdict(set)  # page → indexes of the lines in a decision's quote
    acs = defaultdict(list)  # code → pages
    refs = defaultdict(list)  # own id → [pages, in order of appearance]
    external = defaultdict(list)  # (project, id) → [pages]
    folders, rows = read_external_references(pages.get("external-references.md"), r)
    projects = set(folders) | {k[0] for k in rows}

    for rel, p in pages.items():
        ac_section = p.section_lines("Acceptance Criteria")
        group = None
        for i, line in enumerate(p.prose):
            # Definitions
            m = DECISION.search(line)
            if m:
                d = m.group("id")
                defs[d].append((rel, i))
                quote = []
                for j in range(i, len(p.prose)):
                    if not p.lines[j].startswith(">"):
                        break
                    quote.append(p.prose[j])
                    quoted[rel].add(j)
                if not line.startswith(">"):
                    r.problem(rel, f"{d} is not in a quote block")
                state = STATES.get((m.group("state") or " ")[0])
                door = "⛔️" if m.group("door") else ""
                if state is None:
                    r.problem(rel, f"{d} has no state: `🔀❗️{door}` to decide, `🔀ℹ️{door}` FYI or `🔀✅{door}` done")
                elif (m.group("sp1") and (m.group("state") or m.group("door"))) or (m.group("sp2") and m.group("door")):
                    r.problem(rel, f"{d}: no space between the marks (`🔀❗️⛔️`)")
                if any(x and x[0] in "❗ℹ⛔" and not x.endswith("\ufe0f") for x in (m.group("state"), m.group("door"))):
                    r.warn(rel, f"{d}: a mark without its variation selector (U+FE0F) – searches for `🔀❗️⛔️` miss it")
                raw_title = re.search(rf"\*\*{d} – (.+?)\*\*", p.lines[i])  # with its inline code, as indexed
                title = (raw_title.group(1) if raw_title else m.group("title")).strip().rstrip(".")
                decisions[d] = (rel, i, title, bool(m.group("door")), quote, state)
            for m in re.finditer(r"🧪 \*\*(Part of )?(S\d{2}) – ", line):
                (spike_parts if m.group(1) else defs)[m.group(2)].append((rel, i))
            for m in re.finditer(r"❓ \*\*(Q\d{3})\*\* – ", line):
                defs[m.group(1)].append((rel, i))
            m = re.match(r"### 🏁 (M\d{2}) – ", line)
            if m:
                defs[m.group(1)].append((rel, i))
                if rel != "roadmap.md":
                    r.problem(rel, f"{m.group(1)} is defined outside roadmap.md")
            # Acceptance criteria and their milestone groups
            if ac_section and i in ac_section:
                g = re.match(r"(?:All 🏁 (M\d{2})\.|\*\*🏁 (M\d{2})\*\*)", line)
                if g:
                    group = g.group(1) or g.group(2)
                if re.match(r"\s*- (Given|When) ", line):
                    r.problem(rel, f"line {i + 1}: acceptance criterion without 🧐 and ID")
            for m in re.finditer(r"🧐 \*\*(AC-([A-Z]+)-(\d+))\*\*", line):
                ac, code = m.group(1), m.group(2)
                defs[ac].append((rel, i))
                if rel not in acs[code]:
                    acs[code].append(rel)
                if len(m.group(3)) != 2:
                    r.problem(rel, f"{ac}: the number has two digits")
                if not re.match(rf"- 🧐 \*\*{ac}\*\* – Given ", line):
                    r.warn(rel, f"{ac}: form is `- 🧐 **{ac}** – Given …`")
                if not ac_section or i not in ac_section:
                    r.problem(rel, f"{ac} is outside the `## Acceptance Criteria` section")
                elif group is None:
                    r.problem(rel, f"{ac} and those after it come before any `**🏁 M…**` or `All 🏁 M….` line")
                    group = "(reported)"
                if rel.startswith("vision/"):
                    r.problem(rel, f"{ac}: vision pages have no acceptance criteria")
            # References, own or another project's. Quoted text is an example or USER's words, not a reference.
            line = re.sub(r'"[^"]*"|“[^”]*”', lambda q: " " * len(q.group()), line)
            spans = []
            for m in XREF.finditer(line):
                spans.append(m.span())
                for x in expand_ids(m.group(2)):
                    external[(m.group(1), x)].append(rel)
                if line[m.end():].startswith("]("):
                    r.problem(rel, f"line {i + 1}: `↗️ {m.group(1)} {m.group(2)}` – never as a link")
            for m in ID_RE.finditer("" if rel == "external-references.md" else line):  # its IDs are the others'
                if any(a <= m.start() < b for a, b in spans):
                    continue
                name = project_before(line[: m.start()], projects)
                if name and name != own_name:
                    if name in projects:
                        r.problem(rel, f"line {i + 1}: `{name} {m.group(1)}` – write `↗️ {name} {m.group(1)}`")
                    else:
                        r.warn(rel, f"line {i + 1}: `{name} {m.group(1)}` – another project's ID? Then `↗️ {name} {m.group(1)}`")
                    continue
                if name == own_name:
                    r.warn(rel, f"line {i + 1}: `{name} {m.group(1)}` – this project's IDs are written bare")
                refs[m.group(1)].append(rel)
            for m in re.finditer(rf"(?i:\b(?:its|their))( {ID}(?:(?:–|, | and ){ID})*)", line):
                r.warn(rel, f"line {i + 1}: `its/their{m.group(1)}` – another project's ID? Then `↗️ {{Project}}{m.group(1)}`")
            for m in re.finditer(r"\b([DQ]\d{1,2}|[SM]\d|AC-[A-Z]+-\d)\b", line):
                r.warn(rel, f"line {i + 1}: `{m.group(1)}` – old-width ID? (D/Q 3 digits, S/M/AC 2)")

    for k, where in defs.items():
        if len(where) > 1:
            r.problem(where[0][0], f"{k} defined {len(where)} times: " + ", ".join(f"{p}:{i + 1}" for p, i in where))
    for k in sorted(refs):
        if k not in defs:
            r.problem(refs[k][0], f"{k} is referenced but never defined")
    check_external(external, folders, rows, "external-references.md" in pages, r)
    for s, where in spike_parts.items():
        if s not in defs:
            r.problem(where[0][0], f"`Part of {s}` but {s} is defined nowhere")
    for code, where in acs.items():
        if len(where) > 1:
            r.problem(where[0], f"AC code {code} used on several pages: {', '.join(where)}")
    codes_per_page = defaultdict(set)
    for code, where in acs.items():
        for rel in where:
            codes_per_page[rel].add(code)
    for rel, codes in codes_per_page.items():
        if len(codes) > 1:
            r.warn(rel, f"several AC codes on one page: {', '.join(sorted(codes))}")

    # Spikes: defined where first needed, listed in the roadmap.
    roadmap = pages.get("roadmap.md")
    for s in sorted(k for k in defs if k.startswith("S")):
        def_page = defs[s][0][0]
        first = min(refs.get(s, []) + [def_page], key=lambda rel: order[rel])
        if first != def_page:
            r.warn(def_page, f"{s} is defined here, but first mentioned on {first} (defined where first needed?)")
        if roadmap and s not in "\n".join(roadmap.prose):
            r.problem("roadmap.md", f"{s} is not listed")

    # Decisions: their form, and decisions.md.
    for d, (rel, i, title, one_way, quote, state) in sorted(decisions.items()):
        text = "\n".join(quote)
        has_exit = "_Cheap exit:_" in text or "_No cheap exit:_" in text
        if one_way and not has_exit and state != "❗️":
            r.problem(rel, f"{d} ⛔️ has no `_Cheap exit:_` (or `_No cheap exit:_`)")
        if not one_way and "_Cheap exit:_" in text:
            r.warn(rel, f"{d} has a `_Cheap exit:_` but no ⛔️")
        if state == "❗️" and "_Decision:_" in text:
            r.problem(rel, f"{d} is ❗️ but has a `_Decision:_`: then it's ℹ️ (AI's) or ✅ (USER's)")
        if state in ("ℹ️", "✅") and "_Options:_" in text and "_Decision:_" not in text:
            r.warn(rel, f"{d} has options but no `_Decision:_` saying which")
        if state in ("ℹ️", "✅") and "_Recommendation:_" in text:
            r.warn(rel, f"{d} is {state} but has a `_Recommendation:_` – that's for ❗️; decided, it's the `_Decision:_`")
        if state == "✅" and any(INFO_BULLET.match(l) for l in quote[1:]):
            r.problem(rel, f"{d} is ✅ but has ℹ️ bullets: ℹ️ until USER agreed to them")
        if any("🧞" in l for l in quote) and not any("🤠" in l or "🪤" in l for l in quote):
            r.warn(rel, f"{d} holds a 🧞‍♂️ but no 🤠 / 🪤 it replies to: a proposal is an ℹ️ (applied) or a ❗️ (not)")
        if re.search(r"_Options:_.*\(a\).*\(b\)", text):
            r.problem(rel, f"{d}: options inline – the form has one `>     - (a) **{{Option}}** …` sub-bullet each")
    check_index(pages, "decisions.md", "Decision", r"D\d{3}", decisions, defs, r)
    check_index(pages, "open-questions.md", "Question", r"Q\d{3}", None, defs, r)
    if roadmap:
        for rel in ("Later", "Incubation"):
            if roadmap.section_lines(rel) is None:
                r.warn("roadmap.md", f"no `## {rel}` section")
        for n, (i, level, text, _) in enumerate(roadmap.headings):
            if text.startswith("🏁 "):
                end = next((h[0] for h in roadmap.headings[n + 1:] if h[1] <= level), len(roadmap.lines))
                if not any("It is reached when" in l for l in roadmap.prose[i:end]):
                    r.warn("roadmap.md", f"`{text[:30]}…` has no “It is reached when”")
    check_replies(pages, quoted, r)


def expand_ids(text):
    """`D008–D010` → D008, D009, D010; `D014, D015` → D014, D015."""
    out = []
    for part in re.split(r", | and ", text):
        a, _, b = part.partition("–")
        if b and a[0] == b[0] and a[1:].isdigit() and b[1:].isdigit():
            out += [f"{a[0]}{n:0{len(a) - 1}d}" for n in range(int(a[1:]), int(b[1:]) + 1)]
        else:
            out += [a] + ([b] if b else [])
    return out


def read_external_references(page, r):
    """Project lines → {project: docs folder}; table rows → {(project, id): (mark, path, title, line)}."""
    folders, rows = {}, {}
    if not page:
        return folders, rows
    if not any(l.strip() == "| Project | Reference | Page | Title |" for l in page.lines):
        r.problem(page.rel, "no `| Project | Reference | Page | Title |` table")
    for i, line in enumerate(page.lines):
        m = re.match(r"- (.+?) – `([^`]+)`\s*$", line)
        if m:
            folders[m.group(1)] = m.group(2)
            if m.group(2).startswith("/Users/") or m.group(2).startswith("/home/"):
                r.warn(page.rel, f"line {i + 1}: use `~` for the home folder")
            continue
        m = re.match(r"\| (?!Project \|)(.+?) \| (\S+) (\S+) \| (.+?) \| (.+?) \|$", line)
        if m and not line.startswith("| ---"):
            project, mark, ref, path, title = m.groups()
            if (project, ref) in rows:
                r.problem(page.rel, f"`{project} {ref}` listed twice")
            rows[(project, ref)] = (mark, path, title, i)
    return folders, rows


def check_external(used, folders, rows, has_page, r):
    where = "external-references.md"
    if used and not has_page:
        r.problem(where, f"missing, while {len(used)} ↗️ reference(s) are used")
        return
    marks = {"D": "🔀", "Q": "❓", "S": "🧪", "M": "🏁", "A": "🧐"}
    for key, pages in sorted(used.items()):
        if key not in rows:
            r.problem(pages[0], f"`↗️ {key[0]} {key[1]}` has no row in {where}")
    for (project, ref), (mark, path, title, i) in sorted(rows.items()):
        line = f"line {i + 1}: `{project} {ref}`"
        if (project, ref) not in used:
            r.warn(where, f"{line} – used on no page")
        if project not in folders:
            r.problem(where, f"{line} – no `- {project} – `{{docs folder}}`` line above the table")
        if marks.get(ref[0]) not in mark:
            r.problem(where, f"{line} – the mark should be {marks.get(ref[0], '?')}")
        if not re.fullmatch(r"`[^`]+\.md`", path):
            r.problem(where, f"{line} – the page is a `path.md` in code, relative to that project's docs folder")
            continue
        folder = Path(folders.get(project, "/nonexistent")).expanduser()
        if folder.is_dir():  # Offline-friendly: only checked when that project is on this machine.
            target = folder / path.strip("`")
            if not target.is_file():
                r.warn(where, f"{line} – {target} doesn't exist: that project moved its docs? (rerun)")
            elif not re.search(rf"\b{re.escape(ref)}\b", target.read_text(encoding="utf-8")):
                r.warn(where, f"{line} – {ref} not found in {target}: renumbered? (rerun)")


def strip_not_project(words):
    while words and words[0] in NOT_PROJECT:
        words = words[1:]
    return " ".join(words)


def project_before(before, projects):
    """The other project's name right before an ID, if any: a run of capitalized words."""
    m = re.search(r"(?<![\w\])])((?:[A-Z][\w.+-]* )+)$", before)
    if not m:
        return None
    run = m.group(1).strip()
    for name in sorted(projects, key=len, reverse=True):
        if run == name or run.endswith(" " + name):
            return name
    words = run.split()
    # One capitalized word opening a sentence ("Meets Q019", "Between M01") is not taken for a project.
    if len(words) == 1 and re.search(r"(^|[.:;!?(–]|\*\*|^[>\s]*[-*|]|\|)\s*$", before[: m.start()]):
        return None
    return strip_not_project(words) or None


def check_index(pages, index, label, id_pattern, decisions, defs, r):
    page = pages.get(index)
    if not page:
        r.problem(index, "missing")
        return
    if not any(l.strip() == f"| ID | {label} | Page |" for l in page.lines):
        r.problem(index, f"no `| ID | {label} | Page |` table")
    listed = {}
    for i, line in enumerate(page.lines):
        m = re.match(rf"\| ([^|]*?)\b({id_pattern})\b([^|]*?) \| (.+?) \| (.+?) \|$", line)
        if not m:
            continue
        before, k, after, title, cell = m.groups()
        marks = (before.strip() + after.strip()).replace("\ufe0f", "")
        listed[k] = i
        if k not in defs:
            r.problem(index, f"{k} is listed but defined nowhere")
            continue
        def_page, def_line = defs[k][0]
        link = LINK.search(cell)
        if not link:
            r.problem(index, f"{k}: no link")
            continue
        f, _, anchor = link.group(2).partition("#")
        if f != def_page:
            r.problem(index, f"{k} links to {f}, but is defined on {def_page}")
        elif not anchor:
            r.problem(index, f"{k}: link to the section, not just the page")
        elif anchor != pages[def_page].section_at(def_line):
            r.warn(index, f"{k} links to #{anchor}, but is defined under #{pages[def_page].section_at(def_line)}")
        if decisions is None and marks:
            r.problem(index, f"{k}: the ID bare, without marks")
        if decisions and k in decisions:
            _, _, def_title, def_one_way, _, state = decisions[k]
            want = f"🔀{state or ''}{'⛔️' if def_one_way else ''}"
            if state is None:  # reported on its page; only the ⛔️ here
                if ("⛔" in marks) != def_one_way:
                    r.problem(index, f"{k}: ⛔️ differs from its definition")
            elif after.strip() or marks != want.replace("\ufe0f", ""):
                r.problem(index, f"{k}: write `{want} {k}`, with the marks of its definition")
            if title.rstrip(".") != def_title:
                r.warn(index, f"{k}: title differs from its definition")
    for k in sorted(defs):
        if re.fullmatch(id_pattern, k) and k not in listed:
            r.problem(index, f"{k} is not listed")


def check_replies(pages, quoted, r):
    """A 🧞‍♂️ only replies to a 🤠 / 🪤: proposals are decisions now (ℹ️ applied, ❗️ not)."""
    oq = pages.get("open-questions.md")
    if oq and oq.section_lines("Proposals Waiting for a Yes/No") is not None:
        r.problem("open-questions.md", "`## Proposals Waiting for a Yes/No` is gone: an applied proposal is an ℹ️ decision, "
                                       "a choice still to make a ❗️ one, anything else a ❓")
    for rel, p in pages.items():
        legend = p.section_lines("Legend") or range(0)
        if any("🤠" in l or "🪤" in l for n, l in enumerate(p.prose) if n not in legend):
            continue
        n = sum("🧞" in l for k, l in enumerate(p.prose) if k not in legend and k not in quoted[rel])
        if n:
            r.warn(rel, f"{n} 🧞‍♂️ but no 🤠 / 🪤 they reply to: a proposal is an ℹ️ or ❗️ decision")


def check_writing(pages, r):
    voice = re.compile(r"\b(I|I'm|I've|I'd|me|my|mine|myself|[Yy]ou|[Yy]our|[Yy]ours|[Yy]ourself|My|Me)\b")
    for rel, p in pages.items():
        legend = p.section_lines("Legend") or range(0)
        for i, line in enumerate(p.prose):
            if not line.strip() or i in legend:
                continue
            text = LINK.sub(r"[\1]", line)
            if line.startswith("#"):
                words = re.sub(r"^#+ ", "", text).split()
                low = [w for w in words[1:] if w[0].islower() and w.strip("*_()") not in SMALL_WORDS]
                if words and words[0][0].islower():
                    low.insert(0, words[0])
                if low:
                    r.warn(rel, f"line {i + 1}: heading not in Title Case ({', '.join(low)})")
            if re.search(r"(?<![*\w])\*(?![*\s])[^*]+?(?<![*\s])\*(?![*\w])", text):
                r.warn(rel, f"line {i + 1}: `*italic*` – use `_italic_`")
            unquoted = re.sub(r'"[^"]*"|“[^”]*”', "", text)
            if " - " in re.sub(r"^[>\s]*[-*] ", "", unquoted):
                r.warn(rel, f"line {i + 1}: ` - ` – use an en dash ` – `")
            m = re.match(r"^(>?)( *)[-*] ", line)
            if m and m.group(2):
                indent = len(m.group(2)) - (1 if m.group(1) else 0)
                if indent % 4:
                    r.warn(rel, f"line {i + 1}: nested list indented by {indent} – use 4 spaces")
            found = sorted(set(voice.findall(unquoted)))
            if found:
                r.warn(rel, f"line {i + 1}: {', '.join(found)} – an actor is USER or AI (quotes, UI labels and app content stay as written)")
            other = {c for c in EMOJI.findall(line) if c not in MARKS}
            if other:
                r.warn(rel, f"line {i + 1}: marks not in the legend: {' '.join(sorted(other))}")


def finish(r, toc=()):
    rank = {rel: n for n, rel in enumerate(toc)}
    for where in sorted(r.items, key=lambda w: (rank.get(w, -1 if w.startswith("_") or w == "(setup)" else 999), w)):
        print(where)
        for kind, msg in sorted(r.items[where], key=lambda x: x[0] != "problem"):
            print(f"  {'✗' if kind == 'problem' else '?'} {msg}")
    p, w = r.count("problem"), r.count("warning")
    print(f"\n{p} problem(s), {w} warning(s)" if p or w else "OK")
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main())
