# Pilot 01 — Evidence Conflict in VLM Damage Assessment

**Research question (RQ4 of GeoReason):** when the visual evidence in a
post-earthquake satellite image and a textual report about the same
building disagree, which one does an open vision-language model trust?

This matters beyond Earth observation. In any risk-assessment pipeline,
a model that silently follows an incorrect text report over what it can
see will send help to the wrong place. Satellite damage assessment is
simply a testbed where this failure is measurable, because I have
field-validated ground truth for every building.

## Data

A subset of my SAR–Optical Earthquake Damage Dataset
(İslahiye, 2023 Kahramanmaraş earthquakes): 256×256 optical patches with
pixel-level damage masks, field-validated. In this subset two classes
appear:

| Class | Meaning |
|---|---|
| 3 | heavy damage |
| 4 | destroyed |

The damaged building is indicated to the model with a **red bounding
box** derived from the mask. The box is an outline, so the pixels the
model must judge remain fully visible. (An earlier version painted the
mask as a filled overlay — that hides the evidence and turns the task
into blob counting; see `../../research-log/`.)

## Conditions

Same image, same question, five text conditions:

| | Condition | Text shown to the model |
|---|---|---|
| A | Image only | — |
| B | Consistent report | field report agreeing with ground truth |
| C | Conflicting report | field report contradicting ground truth |
| D | Conflicting news | same contradiction, news-style phrasing (style informed by my Turkish Disaster GeoNLP dataset) |
| E | Conflict + abstain | as C, but the model may answer "uncertain" |

## Measurements

1. **Accuracy per condition** — does conflicting text lower accuracy?
2. **Flip rate** — among samples answered correctly image-only, how
   often does added text change the answer? This is the core number.
3. **Abstention usage** — given explicit permission, does the model say
   "uncertain" under conflict, or does it still pick a side?

## How to run

```bash
python prepare_samples.py --base satdemo --out pilot_data
python run_experiment.py  --data pilot_data
python analyze_results.py --data pilot_data
```

Or open `pilot01_colab.ipynb` and run top to bottom on a free Colab GPU.

Model: `Qwen/Qwen3-VL-2B-Instruct` (inference only, deterministic
decoding). The model is a constant in `run_experiment.py` — swapping in
a larger Qwen3-VL is a one-line change.

## Known limitations (deliberate, this is a pilot)

- Binary task (classes 3 vs 4 only) — the demo subset contains no
  intact/moderate buildings.
- One model, small n (~40 images × 5 conditions ≈ 200 inference calls).
- Conflict texts are controlled templates, not real reports. Real
  GeoNLP articles are not usable as ground-truth evidence yet because
  their labels are machine-generated; they inform template *style* only.
- Multi-building patches get one box around all damage pixels.

## What this can grow into

Measuring the flip rate is phase one. If the effect is robust, the next
steps are: more models, the full 4-class dataset, SAR as a second
visual modality, and eventually an agentic setup where the model must
actively reconcile conflicting evidence instead of picking a side —
the direction I want to pursue in my PhD.
