# TMLR draft: status

`main.tex` is the author's draft reframed as an investigative report, modeled on
arXiv:2607.16693. It includes both rounds of the author's code-verified answers
and has no `\authornote`s left.

## Current claims

- **RQ1 (text vs. image heads):** differs by model. A layer-level view (Fig. 5,
  Table 5) shows where each model's top heads sit.
- **RQ2 (ablation):** zero-ablating the top-20 heads for either language
  destroys generation in all four models (at most 1% fluent, against 71-76% for
  random heads). The heads are necessary for coherent output, but the ablation
  cannot show they route language. The script-change rates counted the collapse
  as a change of script; they are kept in Appendix E with that explanation.
- **Exploratory (cross-model):** per-language shared positions (Table 2). The
  Qwen pair's 13/16/15 are about what layer placement predicts (about 11/15/15).
  The union-based "18 of 20" and its wrong Jaccard (18/22) are gone.
- **Probes:** data (127 es-en + 173 hi-en images) and the patch-level CV
  leakage are disclosed.
- **Data:** the unused 118 natural sentences are removed from Section 3.

## Experiments that would most strengthen the paper

1. A layer-matched random control for the ablation (the Qwen top-20 heads are
   19-20 of the 24 heads in layers 0-1).
2. Head sets contrasted between languages (Hindi score minus English score)
   instead of absolute top-20 sets.
3. A proper fluency measure (e.g. character error rate against the rendered
   sentence), and counting a script change only when the output is fluent.
4. Rerunning the script probes with folds grouped by image (GroupKFold).
5. A collapse check on the Spanish-English ablation (Table 9).

## Verify before submitting

- The eight new bib entries (authors, venues). They were added from memory.
- The Qwen2.5 report (arXiv:2412.15115): check that Qwen2.5 was not
  initialized from Qwen2 weights.

## Before camera-ready

- Switch to `\usepackage[accepted]{tmlr}` and fill in `\month`, `\year` and
  `\openreview`.
- `deuchar2013bangor` has no publisher.

## Figures

- Main-body charts (overlap, layer placement, fluency) are drawn from the
  author's reported values by `figures/make_figures.py`. If a number changes,
  update it there and rerun `python3 figures/make_figures.py` from `paper/`.
