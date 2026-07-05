# 2026-07-05 — Pilot 01 design, and why I dropped the first attempt

## What I tried first

My first exploratory notebook (kept in `notebooks/exploratory/`) painted
the damage mask as a red overlay on the optical patch and asked a VLM to
count the red regions and name their direction.

## Why I dropped it

Three reasons, in order of severity:

1. **It stopped being an Earth observation experiment.** Painting the
   mask hides the damage pixels, so the model only counts red blobs.
   Any stock photo would test the same thing — my dataset added nothing.
2. **The result is already known.** VLMs being weak at counting and
   orientation is well documented. Reconfirming it with a 2B model is
   validation, not research.
3. **My ground truth was fragile.** Raw connected-component counts treat
   2-pixel noise as a "region", and a single centroid is an ambiguous
   direction label for multi-blob masks.

## What survives from that attempt

- The rotation-consistency reflex (an answer that should be invariant
  under rotation is a free probe) — I will reuse it later.
- The data-loading and mask-handling code.

## The redesign

Pilot 01 now targets the one question my datasets make me uniquely able
to ask: **evidence conflict**. I have field-validated damage labels, so
I can construct controlled disagreements between what the image shows
and what a report claims, and measure which one the model follows.

Key design decisions:

- Red **box outline** instead of filled overlay: the model is told
  where to look without hiding what it must judge.
- Controlled text templates instead of real GeoNLP articles: for a
  conflict experiment I must know exactly what the text claims. GeoNLP
  labels are machine-generated and not yet human-verified, so the
  dataset informs the *style* of the news template only. Honest use
  beats impressive-sounding use.
- Patches with fewer than 15 damage pixels are excluded — asking a
  model to judge 19 pixels is not a fair visual question.
- Deterministic decoding, results appended after every call
  (Colab-disconnect-safe), resume supported.

## What would falsify my expectation

I expect a high flip rate under conflicting text (models tend to trust
text). If the flip rate turns out near zero, that is equally
interesting: it would suggest the model ignores the report entirely,
which is its own failure mode for a decision-support system.
