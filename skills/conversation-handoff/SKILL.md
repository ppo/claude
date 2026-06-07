---
name: conversation-handoff
description: Compacts the current conversation into a dense, machine-readable context document for a fresh Claude session to continue the work. Use whenever the user wants to continue this conversation in a new chat, transfer context to another session, or produce a "pick up where we left off" briefing. Trigger on phrases like "handoff", "continue in a new chat", "context for next session", "summarize for Claude", "I'll resume this later", or any intent to pass the current session's state to a fresh Claude instance — even if the user doesn't use those exact words.
---

# Conversation Handoff

Produces a compact, machine-optimized briefing document from the current conversation. Intended to be pasted at the top of a new Claude session to reconstruct working context accurately and efficiently.

## Principles

- **Dense over readable** – optimize for Claude parsing, not human reading
- **State over history** – capture *where things are*, not the journey (unless `full` preset)
- **Precise over complete** – exact names, values, and decisions matter more than prose narrative
- **No scaffolding** – strip greetings, affirmations, repetition, and conversation filler

## Extraction Model

Always extract all sections internally; render only those required by the active preset.

| Section | What to capture |
|---|---|
| **Context** | What prompted the conversation; initial situation, problem, or goal |
| **Exploration** | Brainstorming, hypotheses, paths considered, questions raised |
| **Findings** | Research results, facts established, insights |
| **Decisions** | Choices made and their rationale |
| **Conclusions** | Final answers, outputs, synthesis |
| **Actions** | Open threads, next steps, commitments |
| **References** | Links, files, code, resources mentioned |

## Detail Presets

Default: **standard**

| Preset | Sections rendered |
|---|---|
| `minimal` | Conclusions + Actions |
| `brief` | Context + Conclusions + Actions |
| `standard` | Context + Findings + Conclusions + Actions + References |
| `full` | All sections |

NL overrides apply on top of the active preset. Examples: *"discard the part about X"*, *"be really thorough about Y"*, *"keep the brainstorming"*, *"just the conclusions"*, *"skip references"*.

## Parsing the Request

Extract from the user's invocation:
1. **Preset** – explicit ("full handoff", "brief") or inferred from context. Default: `standard`.
2. **Next session focus** – if the user says what they'll work on next, surface related context prominently.
3. **NL overrides** – specific inclusions or exclusions stated in plain language.

## Output

Produce as an **artifact**.

Use terse, bullet-heavy formatting. Prefer short declarative statements. Use nested bullets for sub-details. Avoid prose paragraphs except where a decision or conclusion genuinely requires explanation.

```
# Handoff – [one-line session summary]

**Date:** [YYYY-MM-DD]
**Next focus:** [if specified by user – omit line if not]

## Context
[What this conversation was about and why; the starting situation or question]

## Exploration
[full preset only – hypotheses, the thinking process, options/branches considered, questions that arose]

## Findings
[standard/full – established facts, research results, insights/what was learned]

## Decisions
[standard/full – what was chosen and why]

## Conclusions
[The synthesis – what was arrived at; the takeaway]

## Actions
- [ ] [next step or open thread]
- [ ] [...]

## References
- [Label](URL or file path)
- **Label:** Description.
```
