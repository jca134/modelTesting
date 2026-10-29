# GLiNER2.5-Decide Tuning

_Generated 2026-10-15 00:14 by `gliner_tune.py report`._

<!-- top15:start -->
## Top 15 setups

Every setup from both rounds that fits the 5-minute budget, ranked by: fewest high-level files missed (for random reads, the worst of 5 seeds), then balanced score, then speed. Thresholds are cross-validated. Time is model time for one pass over all 122 files on this Mac's CPU; per document = time / 122. When several setups give exactly the same results, only the fastest is listed.

| # | Setup | Time (per doc) | High missed | False positives | Accuracy | Recall | Balanced | Edge-case acc. |
|---|---|---|---|---|---|---|---|---|
| 1 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full` labels, 200-word blocks (50 overlap) | 112 s (0.92 s) | 0/58 | 15/58 | 87% | 98% | 0.86 | 69% |
| 2 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full` labels, 200-word blocks | 83 s (0.68 s) | 0/58 | 16/58 | 86% | 98% | 0.85 | 67% |
| 3 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full` labels, 100-word blocks | 62 s (0.51 s) | 0/58 | 17/58 | 85% | 98% | 0.85 | 67% |
| 4 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full+question` labels, 200-word blocks | 85 s (0.70 s) | 0/58 | 18/58 | 84% | 98% | 0.84 | 62% |
| 5 | Rules + file-name keywords first, then early exit, `p3_full+question` labels, 200-word blocks | 161 s (1.32 s) | 0/58 | 20/58 | 83% | 98% | 0.82 | 58% |
| 6 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full` labels, 50-word blocks | 56 s (0.46 s) | 0/58 | 21/58 | 82% | 98% | 0.81 | 60% |
| 7 | Rules + file-name keywords first, then early exit, `p3_full` labels, 100-word blocks | 165 s (1.36 s) | 0/58 | 21/58 | 82% | 98% | 0.81 | 62% |
| 8 | Rules + file-name keywords first, then early exit, `p3_full` labels, 50-word blocks | 210 s (1.72 s) | 0/58 | 26/58 | 78% | 98% | 0.77 | 56% |
| 9 | Rules first, per-category thresholds, then early exit, `p3_full#small` labels, 200-word blocks | 14 s (0.12 s) | 0/58 | 27/58 | 77% | 98% | 0.76 | 60% |
| 10 | Rules first, per-category thresholds, then early exit, `p3_full#base` labels, 200-word blocks | 53 s (0.44 s) | 0/58 | 29/58 | 75% | 97% | 0.73 | 52% |
| 11 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full#small` labels, 200-word blocks | 8 s (0.07 s) | 0/58 | 41/58 | 66% | 100% | 0.65 | 48% |
| 12 | Rules + file-name keywords first, then early exit, `p3_full#small` labels, 200-word blocks | 10 s (0.08 s) | 0/58 | 44/58 | 64% | 100% | 0.62 | 48% |
| 13 | Every block + rules + file name, `p3_full#small` labels, 200-word blocks | 84 s (0.69 s) | 0/58 | 45/58 | 63% | 100% | 0.61 | 46% |
| 14 | Rules + file-name keywords first, pre-filter blocks, then early exit, `p3_full#base` labels, 200-word blocks | 20 s (0.16 s) | 0/58 | 48/58 | 61% | 100% | 0.59 | 44% |
| 15 | Rules + file-name keywords first, then early exit, `p3_full#base` labels, 200-word blocks | 20 s (0.17 s) | 0/58 | 49/58 | 60% | 100% | 0.58 | 44% |

## Recommendations

**1. Use this setup in the scanner:**

1. Run the pattern rules (`find` in `sensitive_rules.py`) on the file's text. If any rule matches, flag the file and skip the model.
2. Otherwise split the text into consecutive 200-word blocks.
3. Skip every block that has no personal signal (`block_has_signal`: no names, 3+ digit numbers, emails, or sensitive keywords). About half of all blocks are skipped.
4. Score the remaining blocks in order with GLiNER2.5-Decide and the `p3_full` labels (7 categories with full descriptions; see `LABEL_SETS` in `gliner_tune.py`). A block's score is the share of label confidence on the six sensitive categories (`norm_sum`).
5. Stop at the first block scoring ≥ 0.5 and flag the file; if no block reaches 0.5, the file is clear.

Measured: 88 s per pass (0.72 s per document), 0/58 high-level files missed, 16/58 false positives, 86% accuracy.
Without the block pre-filter (rules + early exit only): 162 s per pass (1.32 s per document), 0/58 high-level files missed, 18/58 false positives, 84% accuracy.
Reading every block without rules or early exit: 288 s per pass (2.36 s per document), 1/58 high-level files missed, 18/58 false positives, 84% accuracy. The recommended setup is 70% faster and misses 1 fewer high-level file(s).

**The 0.5 cut-off is safe to fix for the PyTorch model.** In this pipeline every threshold from 0.2 to 0.5 gives identical results (0 missed, 16 false positives), because GLiNER's multi-label block scores sit near 0 or near 1.

**2. If false alarms become the main complaint,** switch the labels to `p5way` (5 merged categories), same pipeline: 74 s per pass (0.61 s per document), 4/58 high-level files missed, 10/58 false positives, 86% accuracy. Fewer false alarms and slightly faster, at the cost of missing some high-level files.

**3. Before shipping, check the browser build.**
The 345 MB q4f16 browser file (`onnx-community/GLiNER2.5-Decide-mobile-ONNX`) in the recommended pipeline: 135 s per pass (1.11 s per document), 2/58 high-level files missed, 16/58 false positives, 84% accuracy (CPU via ONNX Runtime). Quantization and its single-label scoring cost a little accuracy compared with the PyTorch original, and its scores are spread out, so **the threshold matters for the browser build**:

| Threshold (browser file) | High missed | False positives | Accuracy |
|---|---|---|---|
| 0.4 | 0/58 | 33/58 | 73% |
| 0.5 | 0/58 | 25/58 | 80% |
| **0.6** | **0/58** | **18/58** | **85%** |
| 0.7 | 1/58 | 13/58 | 88% |

**Use 0.6 for the browser build.** That value was chosen on these same 122 files, so confirm it on a separate set before shipping, and measure speed in Chrome (WebGPU or WASM).

**What did not help** (details below):

- **Faster hardware paths:** the Mac GPU (slower than CPU), batching a file's blocks (no gain), 8-bit weights (about 2× slower on this CPU), fewer CPU threads (no gain).
- **Other read strategies:** random small blocks (the worst random seed misses up to 7 high-level files), evenly spaced subsets, first-N-words only, overlapping blocks (same accuracy, 25–40% slower), blocks smaller or larger than 200 words.
- **Other labels:** shorter descriptions or names only (11–22 high-level files missed), the question as task name (no gain), 9 narrower labels (over budget).
- **Smaller or other GLiNER models:** `gliner2.5-small-v1`, `gliner2.5-base-v1` and `GLiNER2.5-multi-Decide` are 2–10× faster but flag nearly every file (41–57 of 58 harmless files) (small model in the recommended pipeline: 9 s per pass (0.07 s per document), 0/58 high-level files missed, 41/58 false positives, 66% accuracy). The small model is the best candidate for fine-tuning.
- **Extra signals:** scoring the file name with the model (+46 s, no accuracy gain), a learned combination of category scores (fewer false alarms but misses 2–4 high-level files), per-category thresholds (1 more miss for 2 fewer false alarms), file-name keyword rules (−5 s, no accuracy change), the cascade and hybrid variants.

**Caveats:** the test set has 122 synthetic files, so differences of one or two files are within noise. The pattern rules were written knowing the test set and will catch less on real files. All times are on an Apple M3 CPU; browser speed will differ.

<!-- top15:end -->
Goal: the fastest GLiNER2.5-Decide setup that stays close to the best accuracy. Same 122-file test set and metrics as `RESULTS.md`; the 5-minute budget (300 s per pass) still applies (⛔ = over).

## What was varied

- **Labels:** `p3_full` (benchmark P3), `p3_short` (2–5 word descriptions), `p3_names` (names only), `p5way` (5 merged categories), `p3_plus` (9 narrower labels incl. an explicit "training/policy text about privacy" negative). Suffix `+question`: the question is passed as GLiNER's task name (the benchmark passed a bare `q`). Suffix `+single`: single-label scoring (labels compete in one softmax), as the browser build does.
- **Chunk:** words per block. "200 w, 50 overlap" = 200-word blocks that share 50 words with the next one, so a passage on a boundary appears whole in at least one block.
- **Read:** which blocks are read. *Every chunk* covers the whole file; *first chunk only* = the first N words; *evenly spaced* always includes the first and last block; *random* picks blocks at random (5 seeds; numbers are the average, and *worst seed* shows the most high-level files missed by any seed); *first + random* always reads the first block plus random others. A file is flagged when any block read is flagged. Time is scaled by the share of blocks read.
- **Scoring:** `norm_sum` = share of label confidence on sensitive labels (benchmark rule); `max_vs_none` = strongest sensitive label vs. strongest negative label.
- **Threshold:** picked by 2-fold cross-validation (chosen on half the files, applied to the other half), so no file is scored with a cutoff tuned on itself. The baseline row uses the fixed 0.5.

## Speed findings (measured, `p3_full`, 200-word blocks)

| Setup | Time on the same files |
|---|---|
| CPU, one block per call (benchmark) | 231 s for 82 files |
| CPU, a file's blocks batched in one call | 239 s for 82 files |
| Apple GPU (MPS), batched | 277 s for 65 files (CPU: 160 s for the same 65) |

Neither batching nor the Mac GPU helps, so all tuning runs use the CPU. Speed has to come from reading less text or cheaper labels. Browser speed (ONNX Runtime Web on WebGPU) will differ; the relative effect of reading less carries over.

## Baseline (benchmark setup, fixed 0.5 threshold)

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 200 w | every chunk | norm_sum | 288 s | 0.83 | 84% | 97% | 1.0/58 | 18.0/58 | 62% |

## Recommendation

Most accurate setup within budget:

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p5way | 200 w | 8 evenly spaced | norm_sum | 195 s | 0.84 | 84% | 84% | 7.0/58 | 10.0/58 | 67% |

Fastest setup within 0.02 balanced score and at most one more high-level miss than that (for random reads, on its worst seed):

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 100 w | 8 evenly spaced | norm_sum | 194 s | 0.82 | 83% | 95% | 2.0/58 | 18.0/58 | 60% |

Thresholds picked on each half: best [0.2, 0.2], fastest [0.2, 0.2].


## Chunk size and overlap (every chunk read)

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 200 w | every chunk | norm_sum | 288 s | 0.83 | 84% | 97% | 1.0/58 | 18.0/58 | 62% |
| p3_full | 300 w | every chunk | norm_sum | 306 s ⛔ | 0.81 | 82% | 94% | 3.0/58 | 18.0/58 | 58% |
| p3_full | 100 w | every chunk | norm_sum | 316 s ⛔ | 0.81 | 82% | 98% | 0.0/58 | 21.0/58 | 62% |
| p3_full | 200 w, 50 overlap | every chunk | norm_sum | 393 s ⛔ | 0.84 | 84% | 98% | 0.0/58 | 18.0/58 | 62% |
| p3_full | 100 w, 25 overlap | every chunk | norm_sum | 434 s ⛔ | 0.81 | 82% | 98% | 0.0/58 | 21.0/58 | 60% |
| p3_full | 50 w | every chunk | norm_sum | 513 s ⛔ | 0.77 | 78% | 98% | 0.0/58 | 26.0/58 | 56% |

## Fewer words: first N words only

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 50 w | first chunk only | norm_sum | 55 s | 0.67 | 67% | 64% | 22.0/58 | 17.0/58 | 40% |
| p3_full | 100 w | first chunk only | norm_sum | 59 s | 0.70 | 70% | 64% | 22.0/58 | 14.0/58 | 42% |
| p3_full | 100 w, 25 overlap | first chunk only | norm_sum | 63 s | 0.70 | 70% | 64% | 22.0/58 | 14.0/58 | 42% |
| p3_full | 200 w | first chunk only | norm_sum | 78 s | 0.71 | 70% | 67% | 20.0/58 | 15.0/58 | 44% |
| p3_full | 300 w | first chunk only | norm_sum | 97 s | 0.72 | 72% | 70% | 18.0/58 | 15.0/58 | 44% |
| p3_full | 200 w, 50 overlap | first chunk only | norm_sum | 102 s | 0.71 | 70% | 67% | 20.0/58 | 15.0/58 | 44% |

## Random small chunks

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 50 w | 3 random | norm_sum | 106 s | 0.65 | 65% | 63% | 22.8/58 (worst seed 27) | 19.2/58 | 46% |
| p3_full | 50 w | first + 2 random | norm_sum | 106 s | 0.67 | 67% | 68% | 19.2/58 (worst seed 21) | 20.2/58 | 43% |
| p3_full | 100 w | 3 random | norm_sum | 108 s | 0.74 | 74% | 77% | 14.0/58 (worst seed 19) | 17.0/58 | 55% |
| p3_full | 100 w | first + 2 random | norm_sum | 108 s | 0.74 | 74% | 76% | 14.2/58 (worst seed 17) | 16.0/58 | 50% |
| p3_full | 50 w | 5 random | norm_sum | 145 s | 0.69 | 69% | 73% | 16.4/58 (worst seed 20) | 20.4/58 | 49% |
| p3_full | 50 w | first + 4 random | norm_sum | 145 s | 0.70 | 70% | 76% | 14.2/58 (worst seed 17) | 20.8/58 | 48% |
| p3_full | 100 w | 5 random | norm_sum | 148 s | 0.76 | 76% | 83% | 10.0/58 (worst seed 19) | 18.0/58 | 55% |
| p3_full | 100 w | first + 4 random | norm_sum | 148 s | 0.77 | 78% | 83% | 9.6/58 (worst seed 12) | 16.8/58 | 53% |
| p3_full | 100 w | 10 random | norm_sum | 216 s | 0.79 | 80% | 92% | 4.2/58 (worst seed 14) | 19.4/58 | 60% |
| p3_full | 100 w | first + 9 random | norm_sum | 216 s | 0.81 | 81% | 96% | 1.8/58 (worst seed 7) | 19.8/58 | 62% |
| p3_full | 50 w | 10 random | norm_sum | 233 s | 0.71 | 71% | 81% | 11.0/58 (worst seed 16) | 22.8/58 | 52% |
| p3_full | 50 w | first + 9 random | norm_sum | 233 s | 0.73 | 74% | 84% | 9.0/58 (worst seed 11) | 22.0/58 | 52% |
| p3_full | 100 w | 20 random | norm_sum | 289 s | 0.80 | 81% | 96% | 1.8/58 (worst seed 7) | 20.4/58 | 62% |
| p3_full | 50 w | 20 random | norm_sum | 347 s ⛔ | 0.76 | 76% | 93% | 3.6/58 (worst seed 9) | 24.2/58 | 54% |

## Evenly spaced chunks

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 50 w | 2 evenly spaced | norm_sum | 84 s | 0.67 | 67% | 70% | 18.0/58 | 21.0/58 | 44% |
| p3_full | 100 w | 2 evenly spaced | norm_sum | 84 s | 0.73 | 73% | 72% | 17.0/58 | 15.0/58 | 52% |
| p3_full | 100 w, 25 overlap | 2 evenly spaced | norm_sum | 91 s | 0.74 | 74% | 72% | 17.0/58 | 14.0/58 | 52% |
| p3_full | 200 w | 2 evenly spaced | norm_sum | 118 s | 0.75 | 75% | 75% | 15.0/58 | 15.0/58 | 54% |
| p3_full | 50 w | 4 evenly spaced | norm_sum | 125 s | 0.69 | 70% | 77% | 14.0/58 | 22.0/58 | 44% |
| p3_full | 100 w | 4 evenly spaced | norm_sum | 131 s | 0.75 | 75% | 80% | 12.0/58 | 17.0/58 | 56% |
| p3_full | 200 w, 50 overlap | 2 evenly spaced | norm_sum | 141 s | 0.75 | 75% | 75% | 15.0/58 | 15.0/58 | 54% |
| p3_full | 100 w, 25 overlap | 4 evenly spaced | norm_sum | 143 s | 0.74 | 74% | 75% | 15.0/58 | 16.0/58 | 54% |
| p3_full | 300 w | 2 evenly spaced | norm_sum | 153 s | 0.76 | 76% | 78% | 13.0/58 | 15.0/58 | 54% |
| p3_full | 200 w | 4 evenly spaced | norm_sum | 175 s | 0.76 | 76% | 78% | 13.0/58 | 15.0/58 | 54% |
| p3_full | 100 w | 8 evenly spaced | norm_sum | 194 s | 0.82 | 83% | 95% | 2.0/58 | 18.0/58 | 60% |
| p3_full | 50 w | 8 evenly spaced | norm_sum | 203 s | 0.74 | 75% | 88% | 7.0/58 | 23.0/58 | 50% |
| p3_full | 200 w, 50 overlap | 4 evenly spaced | norm_sum | 208 s | 0.83 | 84% | 92% | 4.0/58 | 15.0/58 | 62% |
| p3_full | 300 w | 4 evenly spaced | norm_sum | 222 s | 0.76 | 76% | 78% | 13.0/58 | 15.0/58 | 54% |
| p3_full | 100 w, 25 overlap | 8 evenly spaced | norm_sum | 228 s | 0.81 | 82% | 95% | 2.0/58 | 19.0/58 | 56% |
| p3_full | 200 w | 8 evenly spaced | norm_sum | 241 s | 0.82 | 83% | 94% | 3.0/58 | 17.0/58 | 60% |
| p3_full | 300 w | 8 evenly spaced | norm_sum | 292 s | 0.81 | 82% | 94% | 3.0/58 | 18.0/58 | 58% |
| p3_full | 200 w, 50 overlap | 8 evenly spaced | norm_sum | 293 s | 0.81 | 82% | 92% | 4.0/58 | 17.0/58 | 58% |

## Label sets and scoring (200-word blocks, every chunk)

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p5way | 200 w | every chunk | norm_sum | 232 s | 0.83 | 84% | 86% | 6.0/58 | 11.0/58 | 67% |
| p5way | 200 w | every chunk | max_vs_none | 232 s | 0.83 | 84% | 86% | 6.0/58 | 11.0/58 | 67% |
| p3_full | 200 w | every chunk | norm_sum | 288 s | 0.83 | 84% | 97% | 1.0/58 | 18.0/58 | 62% |
| p3_full | 200 w | every chunk | max_vs_none | 288 s | 0.83 | 84% | 97% | 1.0/58 | 18.0/58 | 62% |
| p3_full+question | 200 w | every chunk | norm_sum | 291 s | 0.81 | 82% | 97% | 1.0/58 | 20.0/58 | 58% |
| p3_full+question | 200 w | every chunk | max_vs_none | 291 s | 0.81 | 82% | 97% | 1.0/58 | 20.0/58 | 58% |
| p3_names | 200 w | every chunk | norm_sum | 171 s | 0.73 | 73% | 80% | 11.0/58 | 20.0/58 | 58% |
| p3_names | 200 w | every chunk | max_vs_none | 171 s | 0.73 | 73% | 80% | 11.0/58 | 20.0/58 | 58% |
| p3_short | 200 w | every chunk | norm_sum | 230 s | 0.67 | 66% | 61% | 22.0/58 | 16.0/58 | 44% |
| p3_short | 200 w | every chunk | max_vs_none | 230 s | 0.67 | 66% | 61% | 22.0/58 | 16.0/58 | 44% |
| p3_full#small | 200 w | every chunk | norm_sum | 38 s | 0.62 | 64% | 100% | 0.0/58 | 44.0/58 | 48% |
| p3_full#small | 200 w | every chunk | max_vs_none | 38 s | 0.62 | 64% | 100% | 0.0/58 | 44.0/58 | 48% |
| p3_full#base | 200 w | every chunk | norm_sum | 92 s | 0.58 | 60% | 100% | 0.0/58 | 49.0/58 | 44% |
| p3_full#base | 200 w | every chunk | max_vs_none | 92 s | 0.58 | 60% | 100% | 0.0/58 | 49.0/58 | 44% |
| p3_full#multi | 200 w | every chunk | norm_sum | 176 s | 0.51 | 53% | 100% | 0.0/58 | 57.0/58 | 44% |
| p3_full#multi | 200 w | every chunk | max_vs_none | 176 s | 0.51 | 53% | 100% | 0.0/58 | 57.0/58 | 44% |

## CPU speed options and the browser file (every chunk read)

`cpu-int8` = 8-bit dynamic quantization of the model's linear layers; `cpu-tN` = N CPU threads; `onnx-mobile` = the 345 MB q4f16 browser build via ONNX Runtime (single-label softmax scoring).

| Device | Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cpu-t4 | p3_full | 200 w | every chunk | norm_sum | 298 s | 0.83 | 84% | 97% | 1.0/58 | 18.0/58 | 62% |
| onnx-mobile | p3_full | 200 w | every chunk | norm_sum | 425 s ⛔ | 0.81 | 81% | 91% | 4.0/58 | 17.0/58 | 67% |

## Fastest 15 setups within 0.03 balanced score of the best

| Labels | Chunk | Read | Scoring | Time | Balanced | Accuracy | Recall | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| p3_full | 100 w | 8 evenly spaced | norm_sum | 194 s | 0.82 | 83% | 95% | 2.0/58 | 18.0/58 | 60% |
| p3_full | 100 w | 8 evenly spaced | max_vs_none | 194 s | 0.82 | 83% | 95% | 2.0/58 | 18.0/58 | 60% |
| p5way | 200 w | 8 evenly spaced | norm_sum | 195 s | 0.84 | 84% | 84% | 7.0/58 | 10.0/58 | 67% |
| p5way | 200 w | 8 evenly spaced | max_vs_none | 195 s | 0.84 | 84% | 84% | 7.0/58 | 10.0/58 | 67% |
| p3_full | 200 w, 50 overlap | 4 evenly spaced | norm_sum | 208 s | 0.83 | 84% | 92% | 4.0/58 | 15.0/58 | 62% |
| p3_full | 200 w, 50 overlap | 4 evenly spaced | max_vs_none | 208 s | 0.83 | 84% | 92% | 4.0/58 | 15.0/58 | 62% |
| p3_full | 100 w | first + 9 random | norm_sum | 216 s | 0.81 | 81% | 96% | 1.8/58 (worst seed 7) | 19.8/58 | 62% |
| p3_full | 100 w | first + 9 random | max_vs_none | 216 s | 0.81 | 81% | 96% | 1.8/58 (worst seed 7) | 19.8/58 | 62% |
| p3_full | 100 w, 25 overlap | 8 evenly spaced | norm_sum | 228 s | 0.81 | 82% | 95% | 2.0/58 | 19.0/58 | 56% |
| p3_full | 100 w, 25 overlap | 8 evenly spaced | max_vs_none | 228 s | 0.81 | 82% | 95% | 2.0/58 | 19.0/58 | 56% |
| p5way | 200 w | every chunk | norm_sum | 232 s | 0.83 | 84% | 86% | 6.0/58 | 11.0/58 | 67% |
| p5way | 200 w | every chunk | max_vs_none | 232 s | 0.83 | 84% | 86% | 6.0/58 | 11.0/58 | 67% |
| p3_full | 200 w | 8 evenly spaced | norm_sum | 241 s | 0.82 | 83% | 94% | 3.0/58 | 17.0/58 | 60% |
| p3_full | 200 w | 8 evenly spaced | max_vs_none | 241 s | 0.82 | 83% | 94% | 3.0/58 | 17.0/58 | 60% |
| p3_full | 200 w | every chunk | norm_sum | 288 s | 0.83 | 84% | 97% | 1.0/58 | 18.0/58 | 62% |

# Round 2: combining signals

_Generated 2026-10-15 00:15 by `gliner_tune2.py report --scope main`._

Round 2 combines GLiNER's block scores (labels `p3_full`, CPU) with cheap extra signals. All numbers are 2-fold cross-validated: every threshold, cascade cut-off and combiner weight is picked on half the files and scored on the other half. Time = model time for one pass over the 122 files (budget 300 s).

### Methods

| Method | How it works |
|---|---|
| every block / first block only | Read all blocks (or just the first N words); flag if any block's score ≥ threshold |
| + rules | Also flag if `sensitive_rules.py` matches (SSN, card number with valid checksum, API/private keys, password assignments, bank account/routing, DOB, passport/SEVIS). Rules take microseconds |
| + file name | Also flag if the file name alone scores ≥ a (cross-validated) cut-off. One tiny model call per file |
| early exit | Read blocks in order and stop at the first flagged one, so sensitive files finish early |
| rules first | Files matched by a rule are flagged without calling the model at all |
| cascade | Score the first block; if it is clearly sensitive or clearly harmless, stop. Otherwise scan the rest with early exit. The cut-offs are cross-validated |
| learned combination | Logistic regression over GLiNER's per-category scores, rules and file-name scores |

**Caveat:** the rules were written with knowledge of this test set, so their real-world benefit may be smaller. File names here are descriptive by design; real Drive file names are often less helpful.

### Recommendation

**Safest** within budget (fewest high-level files missed, then balanced score, then time):

| Method | Labels | Chunk | Time | Balanced | Accuracy | Recall | Precision | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 200 w, 50 overlap | 112 s | 0.86 | 87% | 98% | 81% | 0/58 | 15/58 | 69% |

**Fastest** with the same number of high-level misses and within 0.02 balanced score of the safest:

| Method | Labels | Chunk | Time | Balanced | Accuracy | Recall | Precision | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 100 w | 62 s | 0.85 | 85% | 98% | 79% | 0/58 | 17/58 | 67% |

**Most balanced** within budget (best trade-off between misses and false alarms):

| Method | Labels | Chunk | Time | Balanced | Accuracy | Recall | Precision | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| rules first, per-category thresholds, then early exit | `p3_full+question` | 200 w | 173 s | 0.89 | 89% | 94% | 87% | 2/58 | 9/58 | 75% |

Settings picked on each half: safest [{'t': 0.2}, {'t': 0.2}], fastest [{'t': 0.2}, {'t': 0.2}], most balanced [{'medical': 0.6, 'student_records': 0.3, 'id_numbers': 0.6, 'financial': 0.3, 'credentials': 0.7, 'legal_hr': 0.3}, {'medical': 0.5, 'student_records': 0.4, 'id_numbers': 0.3, 'financial': 0.3, 'credentials': 0.7, 'legal_hr': 0.3}].

### All methods, sorted by balanced score

| Method | Labels | Chunk | Time | Balanced | Accuracy | Recall | Precision | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| rules first, per-category thresholds, then early exit | `p3_full+question` | 200 w | 173 s | 0.89 | 89% | 94% | 87% | 2/58 | 9/58 | 75% |
| learned combination (logistic regression) | `p3_full` | 200 w, 50 overlap | 439 s ⛔ | 0.88 | 89% | 94% | 86% | 2/58 | 10/58 | 75% |
| rules first, per-category thresholds, then early exit | `p3_full` | 100 w | 177 s | 0.88 | 89% | 95% | 85% | 1/58 | 11/58 | 79% |
| learned combination (logistic regression) | `p3_full` | 200 w | 334 s ⛔ | 0.87 | 88% | 92% | 86% | 3/58 | 10/58 | 77% |
| learned combination (logistic regression) | `p3_full` | 300 w | 352 s ⛔ | 0.87 | 88% | 92% | 86% | 3/58 | 10/58 | 73% |
| rules first, per-category thresholds, then early exit | `p3_full` | 200 w, 50 overlap | 233 s | 0.87 | 88% | 94% | 85% | 3/58 | 11/58 | 75% |
| rules first, per-category thresholds, then early exit | `p5way` | 200 w | 142 s | 0.87 | 87% | 88% | 88% | 5/58 | 8/58 | 71% |
| rules first, per-category thresholds, then early exit | `p3_full` | 300 w | 181 s | 0.87 | 87% | 92% | 84% | 4/58 | 11/58 | 71% |
| learned combination (logistic regression) | `p3_full#base` | 200 w | 138 s | 0.86 | 86% | 80% | 93% | 11/58 | 4/58 | 85% |
| rules first, per-category thresholds, then early exit | `p3_full` | 200 w | 166 s | 0.86 | 87% | 97% | 82% | 1/58 | 14/58 | 67% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 200 w, 50 overlap | 112 s | 0.86 | 87% | 98% | 81% | 0/58 | 15/58 | 69% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 200 w, 50 overlap | 122 s | 0.86 | 87% | 98% | 81% | 0/58 | 15/58 | 69% |
| learned combination (logistic regression) | `p3_full@onnx` | 200 w | 471 s ⛔ | 0.86 | 86% | 88% | 86% | 5/58 | 9/58 | 71% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p5way` | 200 w | 70 s | 0.86 | 86% | 89% | 85% | 4/58 | 10/58 | 69% |
| rules first, pre-filter blocks, then early exit | `p5way` | 200 w | 74 s | 0.86 | 86% | 89% | 85% | 4/58 | 10/58 | 69% |
| every block + rules + file name | `p5way` | 200 w | 278 s | 0.86 | 86% | 91% | 84% | 4/58 | 11/58 | 69% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 200 w | 83 s | 0.85 | 86% | 98% | 80% | 0/58 | 16/58 | 67% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 200 w | 88 s | 0.85 | 86% | 98% | 80% | 0/58 | 16/58 | 67% |
| learned combination (logistic regression) | `p3_full` | 50 w | 559 s ⛔ | 0.85 | 85% | 88% | 85% | 5/58 | 10/58 | 71% |
| rules + file-name keywords first, then early exit | `p5way` | 200 w | 136 s | 0.85 | 85% | 89% | 84% | 4/58 | 11/58 | 67% |
| rules first, then every block with early exit | `p5way` | 200 w | 140 s | 0.85 | 85% | 89% | 84% | 4/58 | 11/58 | 67% |
| every block + rules | `p5way` | 200 w | 232 s | 0.85 | 85% | 89% | 84% | 4/58 | 11/58 | 67% |
| rules first, per-category thresholds, then early exit | `p3_full@onnx` | 200 w | 251 s | 0.85 | 85% | 95% | 80% | 2/58 | 15/58 | 65% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 100 w | 62 s | 0.85 | 85% | 98% | 79% | 0/58 | 17/58 | 67% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 100 w | 66 s | 0.85 | 85% | 98% | 79% | 0/58 | 17/58 | 67% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 100 w, 25 overlap | 67 s | 0.85 | 85% | 98% | 79% | 0/58 | 17/58 | 67% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 100 w, 25 overlap | 71 s | 0.85 | 85% | 98% | 79% | 0/58 | 17/58 | 67% |
| rules first, per-category thresholds, then early exit | `p3_full` | 100 w, 25 overlap | 237 s | 0.84 | 84% | 91% | 82% | 4/58 | 13/58 | 75% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full+question` | 200 w | 85 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| rules first, pre-filter blocks, then early exit | `p3_full+question` | 200 w | 90 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| rules + file-name keywords first, then early exit | `p3_full` | 200 w | 157 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| rules first, then every block with early exit | `p3_full` | 200 w | 162 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| rules + file-name keywords first, then early exit | `p3_full` | 200 w, 50 overlap | 217 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| rules first, then every block with early exit | `p3_full` | 200 w, 50 overlap | 227 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block, early exit | `p3_full` | 200 w, 50 overlap | 272 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full` | 200 w, 50 overlap | 273 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block + rules | `p3_full` | 200 w | 288 s | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block + rules + file name | `p3_full` | 200 w | 334 s ⛔ | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block | `p3_full` | 200 w, 50 overlap | 393 s ⛔ | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block + rules | `p3_full` | 200 w, 50 overlap | 393 s ⛔ | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block + rules + file name | `p3_full` | 200 w, 50 overlap | 439 s ⛔ | 0.84 | 84% | 98% | 78% | 0/58 | 18/58 | 62% |
| every block, early exit | `p5way` | 200 w | 169 s | 0.83 | 84% | 86% | 83% | 6/58 | 11/58 | 67% |
| every block | `p5way` | 200 w | 232 s | 0.83 | 84% | 86% | 83% | 6/58 | 11/58 | 67% |
| learned combination (logistic regression) | `p3_full` | 100 w | 362 s ⛔ | 0.83 | 84% | 88% | 82% | 5/58 | 12/58 | 71% |
| learned combination (logistic regression) | `p3_full` | 100 w, 25 overlap | 481 s ⛔ | 0.83 | 84% | 89% | 81% | 4/58 | 13/58 | 71% |
| rules first, per-category thresholds, then early exit | `p3_full` | 50 w | 240 s | 0.83 | 84% | 91% | 81% | 4/58 | 14/58 | 69% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 300 w | 109 s | 0.83 | 84% | 94% | 79% | 3/58 | 16/58 | 62% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 300 w | 113 s | 0.83 | 84% | 94% | 79% | 3/58 | 16/58 | 62% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full@onnx` | 200 w | 127 s | 0.83 | 84% | 94% | 79% | 2/58 | 16/58 | 69% |
| rules first, pre-filter blocks, then early exit | `p3_full@onnx` | 200 w | 135 s | 0.83 | 84% | 94% | 79% | 2/58 | 16/58 | 69% |
| every block, early exit | `p3_full` | 200 w | 200 s | 0.83 | 84% | 97% | 78% | 1/58 | 18/58 | 62% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full` | 200 w | 209 s | 0.83 | 84% | 97% | 78% | 1/58 | 18/58 | 62% |
| every block | `p3_full` | 200 w | 288 s | 0.83 | 84% | 97% | 78% | 1/58 | 18/58 | 62% |
| rules + file-name keywords first, then early exit | `p3_full@onnx` | 200 w | 242 s | 0.82 | 83% | 94% | 78% | 2/58 | 17/58 | 67% |
| rules first, then every block with early exit | `p3_full@onnx` | 200 w | 250 s | 0.82 | 83% | 94% | 78% | 2/58 | 17/58 | 67% |
| every block + rules | `p3_full@onnx` | 200 w | 425 s ⛔ | 0.82 | 83% | 94% | 78% | 2/58 | 17/58 | 67% |
| every block + rules + file name | `p3_full@onnx` | 200 w | 471 s ⛔ | 0.82 | 83% | 94% | 78% | 2/58 | 17/58 | 67% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full@onnx` | 200 w | 295 s | 0.82 | 83% | 97% | 77% | 1/58 | 19/58 | 62% |
| rules + file-name keywords first, then early exit | `p3_full+question` | 200 w | 161 s | 0.82 | 83% | 98% | 76% | 0/58 | 20/58 | 58% |
| rules first, then every block with early exit | `p3_full+question` | 200 w | 165 s | 0.82 | 83% | 98% | 76% | 0/58 | 20/58 | 58% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full+question` | 200 w | 211 s | 0.82 | 83% | 98% | 76% | 0/58 | 20/58 | 58% |
| every block + rules | `p3_full+question` | 200 w | 291 s | 0.82 | 83% | 98% | 76% | 0/58 | 20/58 | 58% |
| every block + rules + file name | `p3_full+question` | 200 w | 337 s ⛔ | 0.82 | 83% | 98% | 76% | 0/58 | 20/58 | 58% |
| rules + file-name keywords first, then early exit | `p3_full` | 300 w | 170 s | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| rules first, then every block with early exit | `p3_full` | 300 w | 175 s | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| every block, early exit | `p3_full` | 300 w | 213 s | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full` | 300 w | 221 s | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| every block | `p3_full` | 300 w | 306 s ⛔ | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| every block + rules | `p3_full` | 300 w | 306 s ⛔ | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| every block + rules + file name | `p3_full` | 300 w | 352 s ⛔ | 0.81 | 82% | 94% | 77% | 3/58 | 18/58 | 58% |
| learned combination (logistic regression) | `p5way` | 200 w | 278 s | 0.81 | 81% | 78% | 85% | 11/58 | 9/58 | 67% |
| every block, early exit | `p3_full+question` | 200 w | 201 s | 0.81 | 82% | 97% | 76% | 1/58 | 20/58 | 58% |
| every block | `p3_full+question` | 200 w | 291 s | 0.81 | 82% | 97% | 76% | 1/58 | 20/58 | 58% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 50 w | 56 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 50 w | 60 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| rules + file-name keywords first, then early exit | `p3_full` | 100 w | 165 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| rules first, then every block with early exit | `p3_full` | 100 w | 170 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| rules + file-name keywords first, then early exit | `p3_full` | 100 w, 25 overlap | 204 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| every block, early exit | `p3_full` | 100 w | 206 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| rules first, then every block with early exit | `p3_full` | 100 w, 25 overlap | 208 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full` | 100 w | 216 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| every block, early exit | `p3_full` | 100 w, 25 overlap | 255 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full` | 100 w, 25 overlap | 256 s | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| every block | `p3_full` | 100 w | 316 s ⛔ | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| every block + rules | `p3_full` | 100 w | 316 s ⛔ | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| every block + rules + file name | `p3_full` | 100 w | 362 s ⛔ | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 62% |
| every block | `p3_full` | 100 w, 25 overlap | 434 s ⛔ | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| every block + rules | `p3_full` | 100 w, 25 overlap | 434 s ⛔ | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| every block + rules + file name | `p3_full` | 100 w, 25 overlap | 481 s ⛔ | 0.81 | 82% | 98% | 75% | 0/58 | 21/58 | 60% |
| every block, early exit | `p3_full@onnx` | 200 w | 306 s ⛔ | 0.81 | 81% | 91% | 77% | 4/58 | 17/58 | 67% |
| every block | `p3_full@onnx` | 200 w | 425 s ⛔ | 0.81 | 81% | 91% | 77% | 4/58 | 17/58 | 67% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p5way` | 200 w | 196 s | 0.80 | 80% | 78% | 83% | 11/58 | 10/58 | 65% |
| learned combination (logistic regression) | `p3_full+question` | 200 w | 337 s ⛔ | 0.80 | 80% | 80% | 82% | 9/58 | 11/58 | 67% |
| first block + rules + file name | `p5way` | 200 w | 110 s | 0.80 | 80% | 75% | 84% | 14/58 | 9/58 | 60% |
| rules first, cascade (first block, then early-exit scan) | `p5way` | 200 w | 49 s | 0.79 | 79% | 73% | 84% | 14/58 | 9/58 | 58% |
| first block + rules | `p5way` | 200 w | 64 s | 0.79 | 79% | 73% | 84% | 14/58 | 9/58 | 58% |
| learned combination (logistic regression) | `p3_full#small` | 200 w | 84 s | 0.79 | 78% | 66% | 89% | 18/58 | 5/58 | 75% |
| rules first, cascade (first block, then early-exit scan) | `p3_full` | 300 w | 73 s | 0.78 | 78% | 81% | 78% | 11/58 | 15/58 | 52% |
| first block + rules | `p3_full` | 300 w | 97 s | 0.78 | 78% | 81% | 78% | 11/58 | 15/58 | 52% |
| first block + rules + file name | `p3_full` | 300 w | 143 s | 0.78 | 78% | 81% | 78% | 11/58 | 15/58 | 52% |
| rules first, cascade (first block, then early-exit scan) | `p3_full` | 100 w | 45 s | 0.77 | 77% | 78% | 78% | 13/58 | 14/58 | 52% |
| rules first, cascade (first block, then early-exit scan) | `p3_full` | 100 w, 25 overlap | 48 s | 0.77 | 77% | 78% | 78% | 13/58 | 14/58 | 52% |
| first block + rules | `p3_full` | 100 w | 59 s | 0.77 | 77% | 78% | 78% | 13/58 | 14/58 | 52% |
| first block + rules | `p3_full` | 100 w, 25 overlap | 63 s | 0.77 | 77% | 78% | 78% | 13/58 | 14/58 | 52% |
| first block + rules + file name | `p3_full` | 100 w | 105 s | 0.77 | 77% | 78% | 78% | 13/58 | 14/58 | 52% |
| first block + rules + file name | `p3_full` | 100 w, 25 overlap | 109 s | 0.77 | 77% | 78% | 78% | 13/58 | 14/58 | 52% |
| rules first, cascade (first block, then early-exit scan) | `p3_full` | 200 w | 58 s | 0.77 | 77% | 80% | 77% | 12/58 | 15/58 | 52% |
| first block + rules | `p3_full` | 200 w | 78 s | 0.77 | 77% | 80% | 77% | 12/58 | 15/58 | 52% |
| rules first, cascade (first block, then early-exit scan) | `p3_full` | 200 w, 50 overlap | 80 s | 0.77 | 77% | 80% | 77% | 12/58 | 15/58 | 52% |
| first block + rules | `p3_full` | 200 w, 50 overlap | 102 s | 0.77 | 77% | 80% | 77% | 12/58 | 15/58 | 52% |
| first block + rules + file name | `p3_full` | 200 w | 125 s | 0.77 | 77% | 80% | 77% | 12/58 | 15/58 | 52% |
| first block + rules + file name | `p3_full` | 200 w, 50 overlap | 148 s | 0.77 | 77% | 80% | 77% | 12/58 | 15/58 | 52% |
| rules + file-name keywords first, then early exit | `p3_full` | 50 w | 210 s | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| rules first, then every block with early exit | `p3_full` | 50 w | 214 s | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full` | 50 w | 260 s | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| every block, early exit | `p3_full` | 50 w | 273 s | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| every block | `p3_full` | 50 w | 513 s ⛔ | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| every block + rules | `p3_full` | 50 w | 513 s ⛔ | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| every block + rules + file name | `p3_full` | 50 w | 559 s ⛔ | 0.77 | 78% | 98% | 71% | 0/58 | 26/58 | 56% |
| learned combination (logistic regression) | `p3_full#multi` | 200 w | 222 s | 0.76 | 75% | 61% | 89% | 21/58 | 5/58 | 75% |
| rules first, per-category thresholds, then early exit | `p3_full#small` | 200 w | 14 s | 0.76 | 77% | 98% | 70% | 0/58 | 27/58 | 60% |
| rules first, cascade (first block, then early-exit scan) | `p3_full+question` | 200 w | 59 s | 0.75 | 75% | 80% | 75% | 12/58 | 17/58 | 48% |
| first block + rules | `p3_full+question` | 200 w | 78 s | 0.75 | 75% | 80% | 75% | 12/58 | 17/58 | 48% |
| first block + rules + file name | `p3_full+question` | 200 w | 124 s | 0.75 | 75% | 80% | 75% | 12/58 | 17/58 | 48% |
| rules first, cascade (first block, then early-exit scan) | `p3_full@onnx` | 200 w | 202 s | 0.75 | 75% | 81% | 74% | 10/58 | 18/58 | 54% |
| rules first, cascade (first block, then early-exit scan) | `p3_full` | 50 w | 42 s | 0.74 | 75% | 78% | 75% | 13/58 | 17/58 | 50% |
| first block + rules | `p3_full` | 50 w | 55 s | 0.74 | 75% | 78% | 75% | 13/58 | 17/58 | 50% |
| first block + rules + file name | `p3_full` | 50 w | 101 s | 0.74 | 75% | 78% | 75% | 13/58 | 17/58 | 50% |
| first block + rules | `p3_full@onnx` | 200 w | 122 s | 0.74 | 74% | 75% | 75% | 14/58 | 16/58 | 52% |
| rules first, per-category thresholds, then early exit | `p3_full#base` | 200 w | 53 s | 0.73 | 75% | 97% | 68% | 0/58 | 29/58 | 52% |
| first block + rules + file name | `p3_full@onnx` | 200 w | 168 s | 0.73 | 73% | 75% | 74% | 14/58 | 17/58 | 50% |
| first block only | `p3_full` | 300 w | 97 s | 0.72 | 72% | 70% | 75% | 18/58 | 15/58 | 44% |
| first block only | `p5way` | 200 w | 64 s | 0.72 | 71% | 59% | 81% | 23/58 | 9/58 | 50% |
| first block only | `p3_full` | 200 w | 78 s | 0.71 | 70% | 67% | 74% | 20/58 | 15/58 | 44% |
| first block only | `p3_full` | 200 w, 50 overlap | 102 s | 0.71 | 70% | 67% | 74% | 20/58 | 15/58 | 44% |
| first block only | `p3_full` | 100 w | 59 s | 0.70 | 70% | 64% | 75% | 22/58 | 14/58 | 42% |
| first block only | `p3_full` | 100 w, 25 overlap | 63 s | 0.70 | 70% | 64% | 75% | 22/58 | 14/58 | 42% |
| first block only | `p3_full+question` | 200 w | 78 s | 0.69 | 69% | 67% | 72% | 20/58 | 17/58 | 40% |
| first block only | `p3_full` | 50 w | 55 s | 0.67 | 67% | 64% | 71% | 22/58 | 17/58 | 40% |
| first block only | `p3_full@onnx` | 200 w | 122 s | 0.66 | 66% | 61% | 70% | 23/58 | 17/58 | 42% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full#small` | 200 w | 8 s | 0.65 | 66% | 100% | 61% | 0/58 | 41/58 | 48% |
| rules first, pre-filter blocks, then early exit | `p3_full#small` | 200 w | 9 s | 0.65 | 66% | 100% | 61% | 0/58 | 41/58 | 48% |
| rules first, cascade (first block, then early-exit scan) | `p3_full#small` | 200 w | 8 s | 0.63 | 65% | 89% | 61% | 7/58 | 36/58 | 42% |
| first block + rules | `p3_full#small` | 200 w | 10 s | 0.63 | 65% | 89% | 61% | 7/58 | 36/58 | 42% |
| first block + rules + file name | `p3_full#small` | 200 w | 56 s | 0.63 | 64% | 89% | 61% | 7/58 | 37/58 | 40% |
| rules + file-name keywords first, then early exit | `p3_full#small` | 200 w | 10 s | 0.62 | 64% | 100% | 59% | 0/58 | 44/58 | 48% |
| rules first, then every block with early exit | `p3_full#small` | 200 w | 10 s | 0.62 | 64% | 100% | 59% | 0/58 | 44/58 | 48% |
| every block, early exit | `p3_full#small` | 200 w | 14 s | 0.62 | 64% | 100% | 59% | 0/58 | 44/58 | 48% |
| every block | `p3_full#small` | 200 w | 38 s | 0.62 | 64% | 100% | 59% | 0/58 | 44/58 | 48% |
| every block + rules | `p3_full#small` | 200 w | 38 s | 0.62 | 64% | 100% | 59% | 0/58 | 44/58 | 48% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full#small` | 200 w | 57 s | 0.62 | 64% | 100% | 59% | 0/58 | 44/58 | 48% |
| every block + rules + file name | `p3_full#small` | 200 w | 84 s | 0.61 | 63% | 100% | 59% | 0/58 | 45/58 | 46% |
| rules first, cascade (first block, then early-exit scan) | `p3_full#base` | 200 w | 20 s | 0.60 | 61% | 95% | 58% | 3/58 | 44/58 | 44% |
| first block + rules | `p3_full#base` | 200 w | 26 s | 0.60 | 61% | 95% | 58% | 3/58 | 44/58 | 44% |
| first block + rules + file name | `p3_full#base` | 200 w | 72 s | 0.60 | 61% | 95% | 58% | 3/58 | 44/58 | 44% |
| first block only | `p3_full#small` | 200 w | 10 s | 0.59 | 60% | 80% | 59% | 13/58 | 36/58 | 33% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full#base` | 200 w | 20 s | 0.59 | 61% | 100% | 57% | 0/58 | 48/58 | 44% |
| rules first, pre-filter blocks, then early exit | `p3_full#base` | 200 w | 21 s | 0.59 | 61% | 100% | 57% | 0/58 | 48/58 | 44% |
| rules + file-name keywords first, then early exit | `p3_full#base` | 200 w | 20 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| rules first, then every block with early exit | `p3_full#base` | 200 w | 22 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| every block, early exit | `p3_full#base` | 200 w | 30 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full#base` | 200 w | 68 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| every block | `p3_full#base` | 200 w | 92 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| every block + rules | `p3_full#base` | 200 w | 92 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| every block + rules + file name | `p3_full#base` | 200 w | 138 s | 0.58 | 60% | 100% | 57% | 0/58 | 49/58 | 44% |
| first block only | `p3_full#base` | 200 w | 26 s | 0.57 | 58% | 89% | 56% | 7/58 | 44/58 | 38% |
| rules + file-name keywords first, then early exit | `p3_full#multi` | 200 w | 28 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full#multi` | 200 w | 28 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| rules first, then every block with early exit | `p3_full#multi` | 200 w | 30 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| rules first, pre-filter blocks, then early exit | `p3_full#multi` | 200 w | 30 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| every block, early exit | `p3_full#multi` | 200 w | 41 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| hybrid: rules, early exit on strong blocks, learned combination for the rest | `p3_full#multi` | 200 w | 76 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| every block | `p3_full#multi` | 200 w | 176 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| every block + rules | `p3_full#multi` | 200 w | 176 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| every block + rules + file name | `p3_full#multi` | 200 w | 222 s | 0.51 | 53% | 100% | 53% | 0/58 | 57/58 | 44% |
| rules first, cascade (first block, then early-exit scan) | `p3_full#multi` | 200 w | 29 s | 0.50 | 52% | 98% | 52% | 1/58 | 57/58 | 44% |
| first block + rules | `p3_full#multi` | 200 w | 40 s | 0.50 | 52% | 98% | 52% | 1/58 | 57/58 | 44% |
| first block + rules + file name | `p3_full#multi` | 200 w | 86 s | 0.50 | 52% | 98% | 52% | 1/58 | 57/58 | 44% |
| rules first, per-category thresholds, then early exit | `p3_full#multi` | 200 w | 31 s | 0.49 | 52% | 94% | 52% | 2/58 | 55/58 | 44% |
| first block only | `p3_full#multi` | 200 w | 40 s | 0.49 | 52% | 97% | 52% | 2/58 | 57/58 | 44% |

### Fastest 15 within 0.03 balanced score of the best

| Method | Labels | Chunk | Time | Balanced | Accuracy | Recall | Precision | High missed | False pos. | Edge acc. |
|---|---|---|---|---|---|---|---|---|---|---|
| rules + file-name keywords first, pre-filter blocks, then early exit | `p3_full` | 200 w, 50 overlap | 112 s | 0.86 | 87% | 98% | 81% | 0/58 | 15/58 | 69% |
| rules first, pre-filter blocks, then early exit | `p3_full` | 200 w, 50 overlap | 122 s | 0.86 | 87% | 98% | 81% | 0/58 | 15/58 | 69% |
| learned combination (logistic regression) | `p3_full#base` | 200 w | 138 s | 0.86 | 86% | 80% | 93% | 11/58 | 4/58 | 85% |
| rules first, per-category thresholds, then early exit | `p5way` | 200 w | 142 s | 0.87 | 87% | 88% | 88% | 5/58 | 8/58 | 71% |
| rules first, per-category thresholds, then early exit | `p3_full` | 200 w | 166 s | 0.86 | 87% | 97% | 82% | 1/58 | 14/58 | 67% |
| rules first, per-category thresholds, then early exit | `p3_full+question` | 200 w | 173 s | 0.89 | 89% | 94% | 87% | 2/58 | 9/58 | 75% |
| rules first, per-category thresholds, then early exit | `p3_full` | 100 w | 177 s | 0.88 | 89% | 95% | 85% | 1/58 | 11/58 | 79% |
| rules first, per-category thresholds, then early exit | `p3_full` | 300 w | 181 s | 0.87 | 87% | 92% | 84% | 4/58 | 11/58 | 71% |
| rules first, per-category thresholds, then early exit | `p3_full` | 200 w, 50 overlap | 233 s | 0.87 | 88% | 94% | 85% | 3/58 | 11/58 | 75% |
