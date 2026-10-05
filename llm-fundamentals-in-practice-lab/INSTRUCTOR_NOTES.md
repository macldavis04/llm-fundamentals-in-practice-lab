# Instructor Exemplar — LLM Fundamentals in Practice Lab

## Read This First

This is **not a set of real transcripts from running these exercises**. I
don't have API access in the environment used to build this, so I can't
actually execute the live, multi-trial experiments this lab requires
(separate isolated conversations, repeated runs to observe variance,
etc.). Writing out invented "Claude said X" dialogue and presenting it as
real observed output would be exactly the kind of fabrication this lab
exists to teach people to recognize — so I'm not doing that.

What follows instead, for each exercise, is:
- The **expected, well-documented pattern** you should observe, and *why*
  it happens — grounded in how these systems are actually built, not guessed
- What a **strong written observation** looks like, as a model for format
  and depth, not as the "correct" specific content (your actual wording
  will differ, and should — you're describing what *you* saw)

Run the actual exercises yourself. This is a study guide for what to
expect and how to write it up well, not a substitute for doing it.

---

## Part 1: Context Window Experiments

### Exercise 1.1: Memory Across Conversations

**Expected pattern:** Claude will recall the fact within the same
conversation (it's in the context window), and will **not** recall it in a
new, separate conversation — reliably, every time, not "usually."

**Why:** This isn't probabilistic model behavior — it's an architectural
fact. Each conversation is an independent context window with no shared
memory unless a product explicitly implements cross-conversation memory as
a separate feature layered on top (which claude.ai has as an opt-in
feature, worth mentioning if you test with it on vs. off). Without that
layer, a new conversation starts with zero knowledge of any prior one, by
design, not by chance.

**What a strong observation looks like:** Name the specific fact you used,
confirm recall within-conversation, confirm the new conversation had no
knowledge of it, and — this is the part worth actually writing, not just
confirming — connect this explicitly to a client-work implication (e.g.,
"this means I can't assume Claude remembers context from an earlier
session with a client unless I explicitly re-provide it or use a feature
designed for persistence").

### Exercise 1.2: Position Sensitivity in Long Context

**Use the provided `position_test_document.txt`** — a real, ~1,500-word
document with three planted facts at the beginning, middle, and end
(`PROJECT-MOONFISH-7`, `FERNHOLLOW-22`, `COPPERWREN-DRAFT-3`).

**Expected pattern:** This is genuinely the least deterministic exercise in
the lab — unlike Exercise 1.1, this one can vary by run, model, and even
how the facts are phrased. The commonly documented "lost in the middle"
effect suggests information placed in the middle of a long context is
sometimes recalled less reliably than information at the very start or end,
but modern long-context models have gotten meaningfully better at this
than earlier generations, so don't be surprised if all three are recalled
correctly. **The honest, useful outcome here is whatever you actually
observe** — if all three come back perfectly, that's a real and worth-
reporting finding too, not a failed exercise.

**What a strong observation looks like:** State plainly which fact(s), if
any, were recalled less reliably, and — if you have time — try it a second
time with the facts reworded (not just repositioned) to see if wording
specificity affects recall independent of position.

### Exercise 1.3: Context Window Budgeting

**This one has no "right" experimental outcome** — it's a written
reasoning exercise. A strong 3-4 sentence answer names concrete tradeoffs
on both sides: pasting everything is simpler to implement and guarantees
nothing relevant gets excluded, but costs more tokens (and money) per
query, can hit context limits as document count grows, and — per Exercise
1.2's findings — may not even guarantee reliable recall of everything
included. Retrieval (RAG) costs more upfront engineering but scales better
and keeps each individual query's context focused and cheaper.

---

## Part 2: Prompt Sensitivity Experiments

### Exercise 2.1: Vague vs. Specific

**Expected pattern:** The three runs of Prompt A (vague) will typically
vary more from each other in structure and content than the three runs of
Prompt B (specific) — though "vary more" doesn't mean wildly different;
it means the vague prompt gives the model more degrees of freedom in what
to prioritize, so different runs may emphasize different aspects of "tips
for a presentation" (structure vs. delivery vs. slide design, for
instance).

**Why:** A highly specific prompt narrows the space of reasonable
responses. A vague prompt leaves far more open, so run-to-run variation
naturally increases — this isn't the model being unreliable, it's the
prompt itself being underspecified.

**What a strong observation looks like:** Point to something concrete that
varied (e.g., "two of the three vague runs led with body language advice,
the third led with structure — while all three specific runs opened with
something about the first 30 seconds specifically, since I asked for
that").

### Exercise 2.2: The Same Ask, Different Words

**Expected pattern:** Genuinely paraphrased prompts (same underlying ask,
different wording) usually produce broadly similar outputs in *substance*
— but differences in emphasis, tone, ordering, or which examples get used
are common and worth noticing specifically.

**What a strong observation looks like:** If you found a case where
rewording changed the output meaningfully, try to identify *what specific
word or phrase* seemed to shift things — was it a change in formality, an
implied audience, or the order instructions were given in?

### Exercise 2.3: Format Instructions

**Expected pattern:** Claude reliably follows explicit format instructions
(numbered list, table with named columns) far more consistently than it
follows *implicit* expectations when no format is specified at all — the
no-instruction version is the one most likely to vary in structure across
different phrasings of the same underlying question.

**What a strong observation looks like:** Confirm whether the table
request specifically got real column headers matching what you asked for,
not just "a table-like list" — this distinction matters a lot for anyone
piping Claude's output into another system expecting a specific structure.

---

## Part 3: Hallucination Pattern Hunting

### Exercise 3.1: Confidence vs. Accuracy

**Expected pattern:** This is the one exercise where genuine model
behavior varies most and is worth testing carefully rather than assuming
an outcome — well-calibrated hedging on obscure topics is something
Claude is specifically trained toward, but the *degree* of hedging you
observe will depend heavily on exactly how obscure your chosen fact is.

**What a strong observation looks like:** Don't just note whether Claude
hedged — try to independently verify the actual answer if at all possible,
and report whether the confidence level Claude expressed actually matched
whether it turned out to be right. A confident wrong answer is a much
more important finding to flag than a hedged wrong answer.

### Exercise 3.2: Forcing a Fabrication

**Expected pattern:** This is a genuinely real, well-documented failure
mode — models can produce plausible-sounding but fabricated citations,
especially when a prompt's phrasing implies a specific fact or source
exists. This is worth testing directly rather than assuming; phrasing
matters a lot here (a leading question that assumes the fact exists is
more likely to produce fabrication than a neutral one).

**What a strong observation looks like:** If you got a fabricated
citation, try to identify specifically what about it seemed real — a
plausible-sounding publication name, a specific-sounding date, a named
author — since this is exactly the kind of detail that makes fabricated
citations dangerous in real client work: they don't look fabricated.

### Exercise 3.3: The Grounding Fix

**Expected pattern:** Providing real source material and instructing
Claude to answer only from it should measurably improve reliability
compared to Exercise 3.2's ungrounded version — this is the most
reliably observable effect in the whole lab, since grounding genuinely
changes what information the model has available to draw from, not just
how it's phrased.

**What a strong observation looks like:** Explicitly compare the two
answers side by side (ungrounded vs. grounded) rather than just describing
the grounded one in isolation — the contrast is the actual point.

---

## Reflection — One Model Example

*(This is one example of a valid reflection, not "the" correct answer —
your own reflection should be based on what you actually observed, and
will reasonably differ from this.)*

> Based on today's experiments, the rule I'll follow going forward is:
> **never let Claude cite a specific source or statistic I haven't
> independently provided or verified.** In Exercise 3.2, I saw firsthand
> how a fabricated citation can sound completely legitimate — specific,
> confident, and plausible — with nothing in the output itself signaling
> that it wasn't real. That's the scenario that could actually damage
> client trust if it made it into a deliverable unchecked. Exercise 3.3
> showed me the fix is straightforward: when I need Claude to reference a
> specific fact or source, I provide the actual source material directly
> rather than asking it to recall one from memory. It's a small workflow
> change, but it directly targets the failure mode I actually watched
> happen in my own testing today, not just a general caution to "be
> careful."
