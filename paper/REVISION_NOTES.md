# TMLR draft: status

`main.tex` is the author's draft reframed as an investigative report, modeled on
arXiv:2607.16693. The title is a question, there are two research questions plus
one exploratory question, results are reported per model, and Section 7 is a
table giving the strength of evidence for each observation. All data, tables and
figures are unchanged.

## Resolved by the reframing

- **InternVL3-2B ablation:** reported as "no distinguishable effect" across seeds
  (11.7 ± 1.2 vs. 14.0 ± 6.2 control). It is no longer claimed as an effect "in
  every model", and the overlap-vs-ablation mismatch is discussed with two
  candidate explanations (T54u #3, KDop).
- **Cross-model head positions:** moved to an exploratory subsection. It now
  states that head numbering is not comparable across independently trained
  models (otTP #1) and suggests a layer-level comparison instead.
- **What LAHIS measures:** new paragraph in Section 5.2 (T54u #1).
- **What the script-flip metric measures:** new paragraph in Section 5.5
  (T54u comment 3).
- **CLIP related work:** Materzyńska et al. 2022 and Gandelsman et al. 2024 are
  now cited (KDop).
- **Stale text:** "We previously attributed this..." removed. "Other two models"
  fixed. The "1.6 to 8.2x" range dropped from the intro.

## Still needs the author (red `[Author: ...]` notes in the PDF)

1. **Section 3:** state whether the LAHIS sentences are monolingual or
   code-switched (otTP #3, T54u #2).
2. **Section 6.3:** PaliGemma random control is 31% in Table 3 but 7.0 ± 2.8 in
   Table 7. Say which is right.
3. **Section 6.4:** was Qwen2.5 initialized from Qwen2? Consider a
   within-layer head-shuffle control for the cross-model overlap.
4. **Section 2:** add the remaining related work KDop asked for (rendered-text
   readability in VLMs; where OCR information enters the decoder).
5. **Appendix C:** the three 100-sentence seed sets are drawn from 118 sentences,
   so they overlap. Say so.

Remove every `\authornote` before submitting.

## Before camera-ready

- Switch to `\usepackage[accepted]{tmlr}` and fill in `\month`, `\year` and
  `\openreview`.
- `deuchar2013bangor` has no publisher.
