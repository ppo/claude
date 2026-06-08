---
name: conversation-archive
description: Extracts and formats the substance of the current conversation into a clean, human-readable, Notion-compatible artifact for long-term second-brain storage. Use whenever the user wants to save, document, or archive a conversation — in Notion or elsewhere. Trigger on phrases like "archive this", "save this to Notion", "document this conversation", "I want to keep this", "save a summary", "make a record of this", or any intent to preserve the current session's content for future human reference — even if the user doesn't mention Notion explicitly.
---

# Conversation Archive

Produces a clean, human-readable artifact from the current conversation, formatted for Notion and long-term second-brain storage. Designed for a human returning weeks later — organized, readable, and scannable.

## Principles

- **Readable over dense** – write for human retrieval, not machine parsing
- **Structured but not bureaucratic** – use headers and bullets where they genuinely help; prose where it flows naturally
- **Apply the user's formatting preferences** – follow conventions defined in their account profile (language, punctuation, quote style, date format, heading case, etc.)
- **Notion-compatible Markdown** 
    – Standard Markdown only; no HTML
    - Maximum 4 heading levels (CMOS title case)
    - No HR (`---`) to visually separate sections/headings
    - Always use smart quotes `‘’“”` (NOT: `'"«»`)
    - For break in a sentence (similar to `;`), always use `–` (NOT: `—` or `-`)
    - For number range, always use regular dash `-` (example: `1-3`)

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
1. **Preset** – explicit ("full archive", "brief") or inferred from context. Default: `standard`.
2. **Title hint** – if the user names the topic, use it to generate a meaningful page title.
3. **NL overrides** – specific inclusions or exclusions stated in plain language.

## Output

Produce as an **artifact** (Markdown). The user will copy/paste into Notion — into a new page, inside an existing one, or as a standalone file.

Apply all formatting preferences from the user's account profile. For sections with multiple items, prefer bullets. For narrative sections (Context, Conclusions), prefer short prose. Keep tone neutral-professional.

```
# 🧞‍♂️ [Descriptive Title in User's Heading Style]

- **🦴 Metadata**
    - **Date:** [YYYY-MM-DD]
    - **Chat:** [chat name](URL)
    - **Topics:** [comma-separated keywords for searchability]

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
