# TMLR draft: open issues

`main.tex` is the author's draft typeset verbatim in the TMLR template
(anonymous submission mode). The text was not edited. These issues were found
while typesetting and are left for the author to decide.

## Numbers that contradict each other

- **PaliGemma random-head control:** Table 3 gives 31%, and the "3.1x control"
  claim depends on it. Table 6 (seeds) gives 7.0 ± 2.8.
- **InternVL3-2B Hindi ablation:** in Table 6, hi-zero (11.7 ± 1.2) is *below*
  the random control (14.0 ± 6.2). This contradicts three claims: the abstract
  and Section 6.4 ("well above a random-head control in every model"), and
  Appendix C ("direction of every zero-ablation effect is preserved").
- **PaliGemma en-zero:** 18% is below its own 31% control (Table 3). This does
  not fit the claim that zero-ablation clears the control in every case.
- **Intro, "1.6 to 8.2x a random-head control":** the 1.6x is InternVL's 14/9.
  The seed data puts that ratio below 1.

## Reviewer points not yet addressed

- **LAHIS scoring data (otTP #3, T54u #2):** still not stated whether the 100
  scoring sentences per language are code-switched or monolingual, and what
  en/es/hi means in Table 2.
- **Ablation vs. overlap (T54u #3, KDop):** InternVL3-2B has the most unified
  routing but the weakest ablation effect. This is still not discussed.
- **Comparing head indices across independently trained models (otTP #1):**
  RQ2 is still framed as "the more important result", and the argument that
  heads within a layer are permutation-invariant is not answered.
- **LAHIS specificity (T54u #1):** LAHIS scores general loss importance, not
  language identity specifically.
- **Missing related work (KDop):** VLM text-readability work, CLIP spelling
  vs. scene disentanglement (Materzyńska et al.; Gandelsman et al.), and work
  on where OCR information enters the decoder.

## Stale or anonymity-breaking text

- **Section 6.4, "We previously attributed this...":** refers to the earlier
  submission. Remove it for double-blind review.
- **Section 6.2, "than the other two models":** there are four models now.
- **Section 6.4, "than the other two models (37/100 against 5/100 and 11/100)":**
  PaliGemma's baseline is missing.
- **Appendix C, "independent random 100-sentence set":** each set is drawn
  from the 118 held-out sentences, so the three sets overlap heavily.

## Before camera-ready

- Switch to `\usepackage[accepted]{tmlr}` and fill in `\month`, `\year` and
  `\openreview`.
- `deuchar2013bangor` has no publisher.
