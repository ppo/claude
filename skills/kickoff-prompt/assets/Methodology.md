# Pascal's Methodology

*How I think and work – for an AI collaborator analyzing, specifying or building one of my projects.*
*Distilled from my "Andy Lab Book" (Notion, Oct 2026). Read it once, apply it everywhere.*


## In One Minute

- My mind is **butterfly-eagle**: I wander freely, then see the whole from high altitude, then dive fast and precise. It looks chaotic; it is organized.
- I use a **toolbox, not a process**: no phases, no fixed order. **Order comes only from dependencies** – what rests on what.
- **Effort follows reversibility**: deep analysis for one-way doors (expensive to undo), fast decisions for two-way doors (cheap to walk back).
- **Build just-in-time, minimal required. Understand enough, not everything.**
- My gap is the **beaver** – finishing and building. Help me land things, not just map them.


## Philosophy

- **Fluidity over speed** – constant progress, even slow; never stuck.
- **Understand enough, not everything** – enough to make informed decisions.
- **Build just-in-time** – when needed, the minimal required.
- **Stronger, not weaker** – I take the stairs, not the escalator: I want to understand what's built for me, not just receive it.
- **In private first** – I work for me; "in public" comes later.


## Butterfly-Eagle

- **Butterfly** – wander: brainstorm, wonder, question freely.
- **Eagle soaring** – high altitude: big picture, architecture, understanding.
- **Eagle diving** – fast and precise: vision, decision, specification.
- Wide first, then narrow – but it loops: a missed dive sends the eagle back up.

Don't impose order on the wandering. Follow it, keep track of loose ends, and bring me back when something load-bearing is waiting.


## Principles

- **Embrace the chaos** – structure emerges from the work; it is never imposed upfront.
- **Toolbox, not process** – moves are used as needed, in any order.
- **Order comes from dependencies** – like a construction site: the foundation comes first because everything rests on it, not because a method says so. Everything else floats.
- **Oscillate between opposites** – progress comes from alternating extremes (wide and deep, high and low, wandering and building), not from staying in the middle.
- **Each work unit has its own rhythm** – foundational (first), transversal (electricity, plumbing), monolithic (kitchen), staged (wiring › connecting › finishing), scattered (demolition, plastering).
- **Effort follows reversibility** – see below.


## One-Way & Two-Way Doors

- **One-way door** – hard to reverse, a **load-bearing wall**: deep analysis upfront, because a mistake means demolition.
- **Two-way door** – cheap to walk back, **furniture placed during the move**: decide fast, fix later.
- **The cheap-exit check** – before committing to a one-way door: *does every risk have a cheap exit?* If not, the decision isn't ready – fly back up.

It's the only gate worth keeping. The same moves serve both: compressed into minutes for a two-way door, given full depth for a one-way door.

Typical one-way doors in my projects: data formats and source of truth, identifiers, storage layout and naming, public interfaces (CLI grammar, APIs, plugin contracts), platform choice, build vs adopt.


## The Graph

A project's knowledge is a **graph**, not a document written top to bottom: it starts as a mind map and grows in every direction, constantly reorganized.

- **Nodes** – elements of knowledge, usually starting as a few questions. Each has a **state** (raw idea › questioned › understood › decided › built; it can move back on a rethink) that shows where things stand, where it's solid and where it's fog, and where attention is needed.
- **Edges** – hierarchy (part of), **dependency** (rests on, blocks), association (relates to, inspired by).
- A node many others rest on is **load-bearing** – that's where depth and care go. A load-bearing node can't be "decided" before it passes the cheap-exit check.


## Moves

Three pairs of opposites – progress comes from oscillating between both ends.

| Animal | Axis | Expansion | Contraction |
| --- | --- | --- | --- |
| Eagle | Altitude | **High** – vision, big picture, rethink | **Dive** – decide, specify |
| Ants | Breadth | **Explore** – scout wide, add nodes and links | **Concentrate** – focus on a find, understand deeply |
| Butterfly ↔ Beaver | Mode | **Wander** – wonder, observe, question | **Build** – make, prototype, test, finish |

The butterfly is my default, the eagle my talent, the beaver my gap. Thinking moves alone produce maps, not things. The beaver builds only because water is flowing – real friction, not hypothetical needs.


## Choosing What's Next

- **Dependencies** – what blocks what, what rests on what.
- **Friction** – what hurts now.
- **Intuition** – what calls in the moment.

⚠️ Without visible dependencies, intuition picks the most interesting job rather than the load-bearing one. Make dependencies visible.


## Course Check

- **Investigating too deeply?** ⇒ Resurface ⇒ Review.
- **Exploring too broadly?** ⇒ Step back ⇒ Big picture.
- **Over-polishing?** ⇒ Minimal required, then improve.
- **Shiny object?** ⇒ Back to the load-bearing work.
- **Stuck?** ⇒ Stop and come back later.


## What This Means for You (AI Collaborator)

- **Let me jump between topics.** Keep a running list of open questions and loose ends; come back to them.
- **Ask in small batches** (1–4 questions), with your recommendation first and a one-line reason.
- **Classify every decision** as a one-way or two-way door. Go deep on one-way doors (options, trade-offs, cheap exits); give a quick recommendation on two-way doors – don't make me deliberate over furniture.
- **Show dependencies.** Tell me what's load-bearing and what rests on what, so order comes from the work, not from habit.
- **Generic thinking, not future-proofing.** Foresee what's obvious, well-known or nearly free; don't design for the unknown. State shared rules as principles to aim for, not strict contracts.
- **Lean, just-in-time.** Specify what the next milestones need; park the rest under "Later / Open". Milestones are usable outcomes, not task lists.
- **Challenge me.** If I'm vague, contradictory, over-engineered or chasing a shiny object, say so plainly and propose a simpler path. My old notes are often brainstorms full of ❓ – treat them as questions, not decisions.
- **Help the beaver.** Push towards something concrete that I'll actually use.
- **I keep control.** Propose; I decide. No changes to my system without my say.
- **Make it understandable.** Explain the why behind important choices, at the level needed to decide – not more.


## My Environment

- Vanlife: often no WiFi for days, 10–15 GB/month of mobile data ⇒ **offline-first and bandwidth-frugal are requirements**.
- MacBook Air M4 (24 GB RAM, 512 GB SSD), iPhone 16 Pro.
- macOS, zsh, iTerm, Homebrew (+ Brewfile), GNU coreutils, Git, VS Code (eyeing Zed). Python with uv; Node via asdf, pnpm.
- French or English.
