# TMLR draft: status

`main.tex` is the author's draft reframed as an investigative report, modeled on
arXiv:2607.16693. It now includes the author's answers about data, head
selection, seeds and baselines, and has no `\authornote`s left.

## What the answers changed

- **Head scoring uses monolingual FLORES sentences.** The title, abstract,
  research questions, Figure 2 and the Data section now say so. Code-switched
  text enters only through the script probes and the ablation.
- **Ablated heads are the absolute top 20 per language, not a contrast.** The
  text no longer calls them "language-selective" and notes that the English
  and Hindi sets overlap heavily.
- **PaliGemma's 31% control was a single draw.** Seed means (control 7.0%) are
  now primary, and the single run moved to Appendix C. PaliGemma's effect is
  about 14x its control, not 3.1x.
- **SmolVLM's ablation produces degenerate output.** Its flips equal its
  baseline Devanagari rate, so RQ2 now has clear effects in two models, not
  three. The Figure 5 bars are annotated.
- **"Held-out" is removed.** The ablation samples 100 of the 806 Hindi-English
  sentences; the 118 natural sentences are a separate set.
- **Baseline Devanagari counts:** 5 (Qwen2-VL-2B), 11 (InternVL3-2B),
  37 (SmolVLM), 15 (PaliGemma-3B).
- **Related work:** added reading-from-pixels and visual-information-flow
  citations (Rust, Tschannen, Kim, Lee, Palit, Basu, Neo).
- **Lineage:** Qwen2.5 is described as a separate pretraining run. Section 6.4
  shows the 18-of-20 match is largely expected, because both models place at
  least 18 of their top 20 heads in layers 0-1 (24 heads). Two such sets must
  share at least 12 positions and would share about 13.5 at random.

## Open questions for the author

1. Are the 806 Hindi-English sentences real GLUECoS data (as the paper says) or
   synthetic?
2. What are the 118 natural sentences used for? If nothing reported, drop them
   from Section 3.
3. Were conditions B/C in head scoring rendered images of the same monolingual
   FLORES sentences?
4. Which sentences do the script probes use, and how many?
5. Which language does "18 of 20 shared positions" refer to (English gives 13)?
   How many of each model's top 20 lie in layers 0-1?
6. Which direction do the script flips go (Latin to Devanagari, or the reverse)
   in Qwen2-VL-2B and PaliGemma-3B?
7. InternVL3-2B's hi-zero rate (11.7) almost equals its baseline Devanagari rate
   (11/100). Does it also coincide with the baseline-Devanagari items, as
   SmolVLM's does? Are Qwen2-VL-2B's and PaliGemma's ablated outputs fluent?

## Verify before submitting

- The eight new bib entries (authors, venues). They were added from memory.
- The Qwen2.5 report (arXiv:2412.15115): check that Qwen2.5 was not
  initialized from Qwen2 weights.

## Before camera-ready

- Switch to `\usepackage[accepted]{tmlr}` and fill in `\month`, `\year` and
  `\openreview`.
- `deuchar2013bangor` has no publisher.

## Figures

- Main-body charts are drawn from the table values by
  `figures/make_figures.py`. If a number changes, update it there and rerun
  `python3 figures/make_figures.py` from `paper/`.
