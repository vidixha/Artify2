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

## Experiments required by the TMLR-style review

The paper now claims only what the current evidence supports. RQ1 is framed as
"does modality change which heads matter" (answered). RQ2 is framed as "are the
heads language-specific" (not answered). These experiments would answer RQ2 and
move the paper toward accept:

1. **Language-specific ablation (critical).** Ablate head sets contrasted
   between languages (top heads by Hindi score minus English score, and the
   reverse), plus random heads matched by layer. Measure teacher-forced loss
   separately on the English and Hindi tokens of each code-switched sentence
   (the gold token labels allow this): Delta L_en and Delta L_hi per head set.
   Routing predicts that Hindi-contrastive heads raise Delta L_hi more than
   Delta L_en, and the reverse for English. Loss-based measures avoid the
   generation collapse.
2. **Layer-matched control.** For each ablated set, draw random heads with the
   same per-layer counts (for Qwen2-VL-2B, mostly from layers 0-1).
3. **Grouped probe evaluation.** Re-run the script probes with GroupKFold by
   image, or with disjoint train and test images.
4. **Script vs. language.** Score heads on transliterated Hindi (Latin script)
   alongside Hindi (Devanagari) and English (Latin), and compare the head sets.
   This separates script from language.
5. **Spanish-English collapse check.** Apply the fluency check to Table 11.

## Before camera-ready

- Switch to `\usepackage[accepted]{tmlr}` and fill in `\month`, `\year` and
  `\openreview`.

## Figures

- Main-body charts (overlap, layer placement, fluency) are drawn from the
  author's reported values by `figures/make_figures.py`. If a number changes,
  update it there and rerun `python3 figures/make_figures.py` from `paper/`.
