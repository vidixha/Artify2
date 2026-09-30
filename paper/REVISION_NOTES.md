# TMLR draft: status

`main.tex` follows the framing and structure of arXiv:2607.16693: a question
title, a page-1 teaser figure, two research questions, Background and
Experimental Setup sections, "Label: finding" result headings, and a
Limitations section after the Conclusion. The prose follows the author's
conference-paper editing rules
(`rules.md`): short active sentences, no mid-sentence colons, semicolons, or em
dashes, takeaway captions, and numbers in tables rather than prose.

## Grounding

Every reference was checked against arXiv, publisher, or proceedings pages.
Changes from earlier drafts:

- InternVL3-2B now cites its own report (arXiv:2504.10479), which lists
  InternViT-300M-448px-V2.5 and Qwen2.5-1.5B.
- The Bangor Miami citation is now Deuchar et al. (2014), "Building bilingual
  corpora" (DOI 10.21832/9781783091713-008). The earlier 2013 "Bangor
  autoglosser" entry could not be found and was removed.
- FLORES-200 now cites the NLLB Team (arXiv:2207.04672).
- Venues were added from arXiv comments and proceedings: Baek (EMNLP 2025), Ye
  (ACL 2025), Nie (Findings of EMNLP 2025), Tang (ACL 2024), Zhai (ICCV 2023),
  Pix2Struct (ICML 2023, PMLR 202), Materzynska (CVPR 2022), Gandelsman
  (ICLR 2024), Basu (NeurIPS 2024), Neo (ICLR 2025). SmolVLM's year is
  corrected to 2025.
- The earlier claim that Qwen2.5 was trained from scratch is removed. The
  Qwen2.5 report states only that pretraining data grew from 7T to 18T tokens.
  It does not say whether Qwen2.5 was initialized from Qwen2.
- The description of Materzynska et al. now matches their abstract.
- Descriptions of Liu et al. (LAHIS), Tang et al., and Wendler et al. now match
  their abstracts. The unsupported claim that Baek et al. studied English text
  only is replaced by what their paper describes (passkey and
  needle-in-a-haystack tasks rendered as images, on Qwen2-VL and InternVL2).
- The LAHIS paper defines its score as E[|m * dL/dm| * 1(dL/dm < 0)]. The paper
  now describes the pipeline's score, |dL/dm| at m = 1 without the
  negative-gradient restriction, as a simplified variant of LAHIS.

## For the author to verify

- Confirm that `stage5_lahis.py` computes |dL/dm| without the
  negative-gradient indicator, as Section 3.2 now states.
- The paper source, with your name and email in `\author`, is in the
  `vidixha/Artify2` repository. The compiled PDF is anonymous. If the repository
  is public, consider making it private during double-blind review.

Model details (layers, heads, encoder sizes) and all results come from the
author's draft and code-verified answers.

## Experiments that would most strengthen the paper

1. A random control drawn from the same layers as the top heads.
2. Head sets contrasted between languages instead of absolute top-20 sets.
3. A proper fluency measure (e.g. character error rate against the rendered
   sentence), with a script change counted only for fluent output.
4. Script probes with folds grouped by image (GroupKFold).
5. A collapse check on the Spanish-English ablation.

## Before camera-ready

- Switch to `\usepackage[accepted]{tmlr}` and fill in `\month`, `\year` and
  `\openreview`.

## Figures

- Main-body charts (overlap, layer placement, fluency) are drawn from the
  author's reported values by `figures/make_figures.py`. If a number changes,
  update it there and rerun `python3 figures/make_figures.py` from `paper/`.
