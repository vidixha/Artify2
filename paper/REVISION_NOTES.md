# Revision Notes: BlackboxNLP → TMLR

## Summary of Changes

This document maps each substantive reviewer concern to its resolution in the
TMLR revision.

---

## Reviewer otTP (Score 1)

### 1. "Comparing head indices across models is only meaningful if models share training"
**Status: Addressed — demoted from headline finding to observation.**

The cross-model head-coordinate comparison (previously Section 7.3, the paper's
second-most-prominent claim) is now explicitly labeled as an "observation" in
Section 7.3 with two paragraphs explaining why it should not be treated as a
finding:
- Head indices across independently trained models require preserved head
  ordering, a strong assumption
- Decoder lineage is confounded with head count, attention mechanism, and
  compression scheme

The Limitations section (paragraph "Decoder lineage") reinforces this. The
contribution list in the Introduction no longer includes lineage as a claim.

### 2. "Methodological contribution is weak — LAHIS applied in a slightly different setup"
**Status: Partially addressed.**

The three-condition framework is now more clearly motivated as a
methodological contribution distinct from LAHIS itself (Section 6.1). A new
paragraph "What LAHIS measures" (Section 6.2) explicitly acknowledges that
LAHIS is not language-identity-specific, which reframes what the method can and
cannot show.

For TMLR (no page limit), we expand the experimental analysis rather than
claiming novel methodology.

### 3. "Not stated which data heads are computed on"
**Status: Fixed.**

Section 3 now has an explicit paragraph ("LAHIS scoring data") stating that
LAHIS scores are computed on monolingual FLORES-200 sentences, not
code-switched data. Section 6.2 repeats this.

### 4. "WWhether" typo
**Status: Fixed.**

---

## Reviewer T54u (Score 2)

### 1. "LAHIS may not localize language-specific heads"
**Status: Addressed head-on.**

New paragraph "What LAHIS measures" in Section 6.2 explicitly states that LAHIS
captures heads important for next-token prediction in a given language, not
language-identity heads specifically. Section 7.3 connects this to the finding
that 14–18 of 20 top heads are shared across languages.

### 2. "Table 3 column labels unclear — what do en/es/hi refer to?"
**Status: Fixed.**

Table 3 (now Table 3 in Section 7.2) has an expanded caption explaining that
en/es/hi indicate "which language's monolingual data was used for LAHIS
scoring." The paragraph preceding the table repeats this.

### 3. "Ablation results run against overlap results (InternVL3-2B)"
**Status: Addressed — this is now a finding, not a gap.**

Section 7.4 now has a dedicated paragraph ("Pathway overlap does not predict
ablation magnitude") that:
- States the prediction explicitly
- Shows the data contradicts it
- Offers a mechanistic explanation (disruption vs. redirection)
- Acknowledges this is a limitation of the script-flip metric
- Identifies what future work would need to measure

This was the single most damaging unaddressed issue in the BlackboxNLP version.

### 4. "Fragmented results, decoder-lineage not relevant to main RQ"
**Status: Addressed — restructured.**

The lineage observation is now a short subsection paragraph within Section 7.3,
clearly marked as observational. The main results flow is: probes → overlap →
cross-language sharing → ablation, each led by the question it answers.

### 5. "Line 497 claim about mean-ablation being 'consistently gentler' contradicts Table 4"
**Status: Fixed.**

The claim is now scoped to "For Qwen2-VL-2B and InternVL3-2B" and the
InternVL3-2B Hindi exception is folded into the mean-ablation anomalies
paragraph.

### 6. "Ablation may show general degradation, not task-specific disruption"
**Status: Acknowledged.**

The "What ablation measures" paragraph in Section 6.5 and the disruption-vs-
redirection discussion in Section 7.4 address this directly.

---

## Reviewer KDop (Score 4)

### 1. "Small grid for lineage claims"
**Status: Addressed by demotion to observation (see otTP #1).**

### 2. "InternVL3-2B near-unified routing contradicts its ablation numbers"
**Status: Addressed (see T54u #3).**

### 3. "PaliGemma contributes little due to small head grid"
**Status: Acknowledged.**

PaliGemma's limited contribution is now stated explicitly in Section 7.2
("PaliGemma-3B shows no strong pattern") with an explanation that the small
grid limits Jaccard resolution.

### 4. "Script probe missing PaliGemma"
**Status: Explained.**

New paragraph in Section 6.4 explains that PaliGemma and SmolVLM share SigLIP-
SO400M, so only three unique encoders are probed.

### 5. "Missing related work on VLM text reading, CLIP"
**Status: Added.**

New "How VLMs read rendered text" paragraph in Related Work citing Tong et al.,
Liu et al., Materzyńska et al., Gandelsman et al., and Neo et al.

### 6. "Single-run, no variance"
**Status: Acknowledged in Limitations.**

"Sample size and variance" paragraph notes that bootstrap resampling would
provide CIs. This is listed as future work rather than done — running new
experiments requires GPU access.

---

## Structural Changes for TMLR

1. Removed page-limit compression; each section is more thorough
2. Added Reproducibility Statement (TMLR requirement)
3. Added Ethics Statement (TMLR recommended)
4. Expanded Limitations section with specific paragraphs for each limitation
5. Reordered contributions: framework → pathway separation → probes → ablation
6. Dropped lineage from contribution list
7. Added "What LAHIS measures" and "What ablation measures" methodological
   caveats throughout

---

## Remaining Work for Resubmission

These items would strengthen the paper but require GPU access / new experiments:

- [ ] Bootstrap CIs on Jaccard overlaps (resample the 100 LAHIS sentences)
- [ ] Generation quality metrics under ablation (perplexity, repetition,
      output length) to test the disruption-vs-redirection hypothesis
- [ ] Run-to-run variance on LAHIS scores (3+ seeds)
- [ ] Consider adding a contrastive attribution method alongside LAHIS
- [ ] Verify the new related-work citations are accurate (Materzyńska et al.,
      Gandelsman et al., Tong et al.) — placeholder entries in references.bib
      need DOIs/full details
