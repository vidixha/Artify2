# New experiments for the TMLR revision

This file is a work order for an agent that has the author's pipeline repository
and a GPU (the original runs used one NVIDIA T4, 16 GB). Each experiment lists
its purpose, procedure, controls, outputs, and how the result enters the paper.

## Background the agent needs

The paper asks two questions about four small VLMs (Qwen2-VL-2B-Instruct,
InternVL3-2B, SmolVLM-Instruct, PaliGemma-3B mix-448):

- **RQ1.** Does input modality change which decoder attention heads are
  important for predicting text in a language? Answered: yes, model-dependent.
- **RQ2.** Are those heads language-specific? **Not answered.** Zero-ablating
  the top-20 heads for either language destroys generation in every model, so
  the current ablation cannot separate language-specific effects from general
  damage. A reviewer judged this the paper's central weakness.

Current method, per the author's description of the pipeline:

- **Head importance** (`stage5_lahis.py`): a soft mask m = 1 on each head's
  output at the input of the attention output projection. Score = |dL/dm|,
  with L the language-modeling loss over all tokens of a sentence. Averaged
  over the first 100 of 250 monolingual FLORES-200 sentences per language
  (`data/monolingual/metadata.json`).
  - Condition A: the text goes through the decoder only.
  - Condition B: the rendered image plus the query "Read this:", with the
    sentence as the target.
  - Condition C: as B, with an empty query.
- **Top heads** (`stage7_patch_locality.py`, `load_top_heads`): the absolute
  top-20 heads by condition-A score, per language.
- **Ablation** (`stage8_ablation.py`, `stage8_ablation_ext.py`):
  - zero or mean ablation at the same hook;
  - greedy generation, 64 tokens, on 100 Hindi-English code-switched images
    sampled from the 806 in `data/codeswitched/metadata.json`;
  - a random control of 20 heads drawn from outside both top-20 sets;
  - one single run (`random.Random(42)`) and seeds 1-3.
- **Script probes** (stage 3 and stage 4):
  - on the first 300 code-switched images (127 es-en, then 173 hi-en), with
    100 patches per image and 4,000 text patches per layer;
  - class-balanced logistic regression, stratified 5-fold cross-validation
    **over patches**, output in `script_probes.json`;
  - transliteration controls are probed in
    `scripts/translit_control_paligemma.py`.
- **Gold labels:** the code-switched sentences have word-level gold language
  labels from GLUECoS.

**Read those files before starting**, and confirm each point above. If any
point is wrong, stop and report the discrepancy before running anything.

## Rules for every experiment

1. **Do not overwrite existing results.** Write everything under
   `results/revision/<experiment_id>/`.
2. **Smoke test first:** 5 sentences, 1 model. Check the shapes, that the
   un-ablated loss matches the existing pipeline, and that the hooks fire.
3. **Record for each run:**
   - model IDs and revisions;
   - library versions;
   - seeds and the exact command, in `run_info.json`.
4. **Fix all random seeds.** Use seeds 0-9 wherever an experiment draws random
   head sets.
5. **Save raw per-sentence values**, not just means. Every statistic must be
   recomputable from the saved files.
6. **Report negative results as they are.** Do not tune thresholds after
   seeing results. Choose them from this file or before looking at the data.
7. **Return:**
   - a `summary.md` per experiment with the tables described below;
   - one overall `REPORT.md` covering what ran, what failed, and deviations
     from this spec.

## Shared definitions

- **Normalized importance.** For model M, language l, and condition c, divide
  each head's score by the sum over all heads:
  s'(h) = s(h) / sum_h s(h). This makes scores comparable across languages.
- **Contrastive head sets (condition A).**
  - The Hindi-contrastive set is the top-k heads by s'_hi(h) - s'_en(h).
  - The English-contrastive set is the top-k by s'_en(h) - s'_hi(h).
  - For Spanish-English, use s'_es and s'_en the same way.
  - Default k = 20. Also run k = 5, 10, 40.
- **Layer-matched random control.** For a target set T with n_l heads in layer
  l, draw n_l heads uniformly from layer l, excluding T. Draw 10 sets
  (seeds 0-9).
- **Token-language assignment.**
  - Map each gold word-level label (hi, en, es, or other, including
    punctuation and named entities) to the target tokens it covers, using the
    tokenizer's offset mapping.
  - Drop tokens that span two words with different labels, and tokens labeled
    other.
  - Report how many tokens are dropped per model.
- **Per-language loss.** Teacher-forced mean NLL over target tokens of one
  language, per sentence: L_hi, L_en, and L_es.
- **Loss change.** Delta L_x = L_x(ablated) - L_x(un-ablated), per sentence.
- **Selectivity.** For a Hindi set, Sel = Delta L_hi - Delta L_en. For an
  English set, Sel = Delta L_en - Delta L_hi.
- **Statistics.**
  - Paired bootstrap over sentences, with 10,000 resamples, for 95% CIs of the
    means.
  - Compare each target set with its 10 layer-matched random sets. Report the
    target value, the random mean and range, and an empirical p-value (the
    fraction of random sets with Sel at least the target's).
  - With 10 random sets the minimum p is about 0.09. If time allows, use 100.

## E1. Language-specific ablation with per-language loss (critical)

**Question:** do some heads affect one language's tokens more than the
other's? This directly tests RQ2 without relying on generation.

**Models:** all four. Language pair: Hindi-English. Condition B is the main
condition. Also run A and C.

**Data:** 200 Hindi-English code-switched sentences from the 806. Use a fixed
seed-0 sample and list the sentence IDs. Every sentence must contain at least
3 hi tokens and 3 en tokens after token-language assignment.

**Head sets:**

1. The Hindi-contrastive and English-contrastive sets (k = 5, 10, 20, 40).
2. The existing absolute top-20 Hindi and English sets, for continuity with
   the current paper.
3. Ten layer-matched random sets for each of the above.
4. Ten whole-network random sets of the same size (the old control).

**Ablations:** zero and mean. Mean ablation replaces each head's output with
its mean over positions in the same input's un-ablated pass, as in the
existing pipeline.

**Measure:** L_hi and L_en per sentence, un-ablated and ablated. Then compute
Delta L_hi, Delta L_en, and Sel.

**Outputs:**

- `e1_per_sentence.parquet` (or `.csv`), with columns: model, condition,
  set_name, k, ablation, seed, sentence_id, L_hi, L_en, dL_hi, dL_en, sel.
- In `summary.md`, one table per model (condition B, k = 20, zero and mean).
  - Rows: Hindi-contrastive, English-contrastive, absolute Hindi, absolute
    English, the layer-matched random mean and range, and the whole-network
    random mean and range.
  - Columns: mean dL_hi, mean dL_en, mean Sel with 95% CI, and the p-value
    against the layer-matched random sets.
- A k-sweep table of Sel for the contrastive sets.

**Interpretation:** record which case holds for each model.

- Hindi-contrastive Sel > 0 and English-contrastive Sel > 0, both above
  layer-matched random: evidence of language-specific heads.
- Both Sel near zero, or within the random range: no evidence of language
  specificity at this granularity.
- Loss rises much more than for layer-matched random, but Sel is near zero:
  necessary but language-general.

**Caveat to state in the report:** Hindi tokens are also Devanagari tokens
here, so language and script are confounded. E1b and E4 address this.

### E1b. Same-script version (Spanish-English)

Repeat E1 on the 127 Spanish-English code-switched sentences, with es and en
token labels and the es/en contrastive sets. Both languages use Latin script,
so a positive Sel here reflects language rather than script. Same outputs, with
the `e1b_` prefix.

## E2. Generation ablation with layer-matched controls and a better fluency measure

**Question:** does the generation collapse (the current Figure 6) exceed what a
fair control produces?

**Procedure:**

- Repeat the existing generation ablation on the same 100 images and seeds.
- Replace the whole-network random control with the layer-matched random
  control (10 draws per target set).
- Add the contrastive sets from E1 (k = 20).

**Outputs per generation:**

- **Character error rate (CER)** against the rendered sentence. The task is
  "Read this:", so the rendered sentence is the reference. Use a standard CER
  implementation, and state which.
- **Empty or letterless flag:** true when the output has no alphabetic
  characters.
- **CJK flag:** true when the output contains any character in the CJK
  Unicode blocks.
- **Repetition rate:** the fraction of repeated 3-grams.
- **Output length** in characters.
- **The existing fluency proxy:** the output keeps at least half of the
  un-ablated output's words.

**Outputs:** `e2_generations.jsonl` holds every output string with its
metadata. `summary.md` has a table per model, with one row per head set and
the mean of each metric with a 95% bootstrap CI.

**Interpretation:** if layer-matched random ablation also collapses output (for
Qwen2-VL-2B, removing about 20 of the 24 heads in layers 0-1), the collapse is
a layer effect. The paper must then say so.

## E3. Script probes with grouped cross-validation

**Question:** does script identity remain decodable when test patches come
from unseen images?

**Procedure:**

- Keep the patch sampling of stage 3 and stage 4.
- Replace patch-level `StratifiedKFold` with `GroupKFold(n_splits=5)`, grouped
  by image ID. `StratifiedGroupKFold` is also acceptable.
- Also run a fixed 80/20 image-level split (seed 0) as a second estimate.
- Everything else is unchanged:
  - probe every vision-encoder layer, for all four models;
  - class-balanced logistic regression;
  - balanced accuracy, with chance at 0.5.
- Re-apply each model's best-layer probe (trained on all code-switched
  images) to the 100 transliteration controls, as before.

**Outputs:** `e3_probes.json`, holding per-layer balanced accuracy for both
evaluation schemes, the old patch-level numbers alongside, and the
transliteration rates. Also regenerate the script-probe figure from the
grouped numbers.

**Enters the paper as:** replacement values for Table 2 and Figure 3.

## E4. Script versus language in head importance

**Question:** does head importance follow script or language?

**Sets to score:** heads in conditions A, B, and C for three sets of 100
sentences each.

1. **English, Latin script:** the existing FLORES-200 English set.
2. **Hindi, Devanagari:** the existing FLORES-200 Hindi set.
3. **Hindi, Latin script:** the same 100 FLORES Hindi sentences, romanized.
   - Preferred: a standard, documented romanization. For example, the
     `indic_transliteration` package (verify that it exists and record the
     scheme). Report the exact scheme.
   - If no acceptable tool exists, use the existing 100 transliteration
     controls and state that their content differs from the Devanagari set.

Render set 3 in Noto Sans, as for all Latin text.

**Competence check first:** compute character-normalized perplexity on set 3.
If a model cannot model romanized Hindi (clearly worse than its worst
language in Table 1), report it and interpret that model's E4 results with
caution.

**Analysis per model and condition:**

- Jaccard overlap of top-20 sets for (Hindi-Latin vs. English-Latin),
  (Hindi-Latin vs. Hindi-Devanagari), and (Hindi-Devanagari vs.
  English-Latin), against the permutation chance level used in the paper.
- The same comparison on contrastive sets (each language against English).

**Interpretation:**

- Hindi-Latin closer to English-Latin: head importance follows script.
- Hindi-Latin closer to Hindi-Devanagari: it follows language.

**Outputs:** `e4_scores.npz` (raw per-head scores), plus the Jaccard tables in
`summary.md`.

## E5. Collapse check on the Spanish-English ablation

**Question:** are the Spanish-English language-change rates in Table 11 also
collapse?

**Procedure:**

- If the Spanish-English ablation outputs are saved, compute the E2 metrics on
  them. This needs no GPU.
- Otherwise, rerun that ablation (the first 100 of the 127 sentences, the same
  head sets, zero ablation) and save the outputs.

**Outputs:**

- Fluent counts, letterless and CJK rates, and CER per model and head set.
- The breakdown of language changes into fluent changes vs. changes caused by
  collapse.

## E6. Variance of the head-overlap values

**Question:** how stable are the Jaccard overlaps in Table 5?

**Procedure:**

- If per-sentence head scores exist, bootstrap the 100 scoring sentences
  (1,000 resamples). Recompute the top-20 sets and the Jaccard overlaps, and
  report 95% CIs.
- If they don't exist, rescore on sentences 100-199 and 150-249 of the 250
  FLORES sentences per language, and report the spread across the three
  subsets.

**Outputs:** `e6_overlap_ci.json`, plus a table matching Table 5 with CIs.

## E7. Robustness to the original LAHIS definition

**Question:** do the RQ1 results change when using the original LAHIS score?

**Background:** the paper uses |dL/dm|. LAHIS (Liu et al., arXiv:2511.07498)
uses E[|m * dL/dm| * 1(dL/dm < 0)] over the corpus.

**Procedure:**

- In the same backward pass, compute the original score per sentence: the
  absolute gradient, set to 0 whenever the gradient is non-negative, then
  averaged.
- Recompute the top-20 sets and Table 5.
- Report the Jaccard overlap between the old and new top-20 sets, per model,
  language, and condition.

**Outputs:** `e7_lahis_original.json`, and a comparison table in `summary.md`.

## E8 (optional, high value). Heads scored on code-switched text

**Question:** do heads scored directly on code-switched input match heads
scored on monolingual input?

**Procedure:**

- Score heads in conditions A, B, and C on the 200 E1 sentences, twice. Once
  restrict the loss to hi tokens, and once to en tokens (same
  token-language assignment as E1).
- Compare these top-20 sets with the monolingual top-20 sets, and rerun the
  RQ1 overlap analysis on them.

**Outputs:** `e8_scores.npz` and overlap tables.

## Priority and rough cost

| Order | Experiment | GPU need | Why |
|---|---|---|---|
| 1 | E1 + E1b | Forward only; about 2 x 8 set types x 11 draws x 200 sentences per model | Decides RQ2 |
| 2 | E2 | Generation; similar to the existing ablation plus the new controls | Tests whether the collapse is a layer effect |
| 3 | E3 | CPU, if the stage-3 features are cached | Fixes probe leakage |
| 4 | E7 | Reuses the E1/E4 backward passes | Defends the LAHIS variant |
| 5 | E4 | Three backward-pass sets | Separates script from language |
| 6 | E5, E6 | Mostly CPU | Closes smaller reviewer points |
| 7 | E8 | Two backward-pass sets | Removes the monolingual-scoring limitation |

## What to return

For each experiment, return:

- the output files;
- `summary.md` with the tables above;
- a short list of anomalies, such as sentences skipped, models that failed, or
  token-assignment drop rates.

Do not edit `paper/main.tex`. The paper will be revised from the returned
numbers.
