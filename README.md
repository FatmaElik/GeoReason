# GeoReason

### Vision-Language Reasoning for Earth Observation and Risk-Aware AI

![Status](https://img.shields.io/badge/status-early--stage%20research-orange)
![Focus](https://img.shields.io/badge/focus-vision--language%20reasoning-blueviolet)
![Type](https://img.shields.io/badge/type-research%20log-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

> **In one sentence.** GeoReason is an open research log where I study how vision-language models reason, ground their claims in evidence, and know when not to answer — using Earth observation as a demanding testbed, not as the research objective.

I am at the beginning of this direction, moving from a background in remote sensing and geospatial AI toward vision-language reasoning, spatial reasoning, trustworthy multimodal AI, and vision-language agents. This repository documents that transition honestly: the questions, the reading, the small experiments, and the dead ends.

---

## What I am studying

The center of this repository is not a specific dataset or disaster type. It is a set of research questions about multimodal AI:

- **Vision-language reasoning:** can a VLM reason about what it sees, or does it produce fluent language that only looks like reasoning?
- **Evidence grounding:** when a model makes a claim, can that claim be tied back to the visual or textual evidence that should support it?
- **Spatial reasoning:** can models reason about where, geometry, orientation, scale, and relations between regions?
- **Risk-aware AI:** can a model recognise when it does not have enough evidence and abstain instead of asserting?
- **Vision-language agents:** can a tool-using VLM decompose a claim, verify it against evidence, and revise itself?

## Why Earth observation?

Earth observation is the testbed because it makes these questions hard and measurable.

Satellite scenes require spatial reasoning. Disaster assessment requires uncertainty. SAR, optical imagery, and text describe the same event from different viewpoints. This makes Earth observation a useful stress test for grounded and risk-aware multimodal AI.

The initial studies build on two datasets that I developed:

1. **SAR–Optical Earthquake Damage Dataset**  
   A multimodal dataset for post-earthquake building damage assessment.

2. **Turkish Disaster GeoNLP Dataset**  
   A Turkish disaster news dataset with geospatial and event-level information for multimodal reasoning experiments.

## Research questions

- **RQ1 — Grounded reasoning vs. fluent guessing:** Do open VLMs reason from evidence, or pattern-match to priors?
- **RQ2 — Spatial reasoning under geometry:** Where do VLMs fail on spatial relations, orientation, and scale?
- **RQ3 — Risk-aware abstention:** Can models be induced to abstain when evidence is insufficient?
- **RQ4 — Multimodal conflict:** What happens when visual evidence and textual reports disagree?
- **RQ5 — From model to agent:** Can a tool-using vision-language agent close gaps that a single forward pass cannot?

## Current pilot

### Pilot 01 — Vision-Language Reasoning under Multimodal Earth Observation Evidence

This pilot uses a small subset of my SAR–optical earthquake damage dataset and Turkish Disaster GeoNLP dataset to probe whether open VLMs remain faithful to evidence when visual and textual signals differ.

The first version is intentionally small:

- 20–50 examples
- no model training
- one open-source VLM
- image-only, text-only, and image+text conditions
- initial focus on failure cases and research questions rather than accuracy

See [`experiments/pilot01-vlm-multimodal-evidence/`](experiments/pilot01-vlm-multimodal-evidence/).

## Research roadmap

```text
Learning → Pilot → Benchmark → Analysis → Method → Vision-Language Agent
```

- **Learning:** literature map, key concepts, open VLM inference pipeline.
- **Pilot:** small experiments on spatial reasoning, grounding, uncertainty, and multimodal conflict.
- **Benchmark:** turn robust failure modes into measurable benchmark tasks.
- **Analysis:** study why failures happen.
- **Method:** prototype evidence-checking, abstention, or grounding mechanisms.
- **Vision-Language Agent:** build a tool-using agent that verifies claims using multimodal evidence.

## Repository structure

```text
GeoReason/
├── research-log/     Dated research notes and working sessions.
├── literature/       Annotated reading notes and bibliography.
├── experiments/      Self-contained pilot experiments.
├── notebooks/        Exploratory notebooks.
├── src/georeason/    Reusable Python utilities.
├── data/             Local data notes only; raw data is not committed.
├── reports/          Technical notes, figures, and write-ups.
├── docs/             Roadmap and design notes.
└── .github/          Issue templates and repository metadata.
```

## Current status

- [x] Repository created
- [x] Research direction defined
- [ ] Literature map in progress
- [ ] Pilot 01 benchmark construction
- [ ] Initial VLM experiments
- [ ] Short technical report

## License

Code in this repository is released under the MIT License.

Datasets are not covered by this license. The SAR–Optical Earthquake Damage Dataset, Turkish Disaster GeoNLP Dataset, and any third-party datasets retain their own usage terms. See [`data/README.md`](data/README.md).

## About

Maintained by Fatma Elik — geophysical engineer working on AI, remote sensing, GeoAI, disaster risk, and multimodal Earth observation.


