# Single-Channel vs Multi-Channel Feature Space

`single_vs_multi_channel_comparison.ipynb` checks whether a multi-channel CIR dataset covers more of the feature space than a single-channel dataset of the same size. It supports the multichannel contribution of the paper, and its last cells draw the per-scenario multi-channel CIR plots used for Fig. 1 (the SIT E2-B2 concrete / glossy wall scenario, 8.41 m LOS and 16.09 m NLOS).

## Data

| File | Channels | Samples |
|---|---|---|
| `../dataset/channels/single_channel5_dataset.csv` | 5 | 100 per scenario, 600 in total |
| `../dataset/channels/multi_channel4_dataset.csv` | 1, 3, 4, 7 | 25 per channel and scenario, 600 in total |

Both sets have 3 LOS and 3 NLOS scenarios. Four are shared (8.41m and 9.76m LOS, 16.09m and 16.80m NLOS); the single-channel set has 4.55m LOS and 12.79m NLOS where the multi-channel set has 9.29m LOS and 9.54m NLOS.

## Method

1. Standardise the 1016-sample CIR and reduce it to 50 components with PCA.
2. Fit UMAP on both sets together so they share one 2D space.
3. Compare the sets with the convex hull area, mean pairwise distance, LOS/NLOS silhouette score, a 15x15 grid occupancy map and the marginal histograms of the two UMAP axes.

## Results (saved outputs)

| Metric | Single-channel | Multi-channel |
|---|---|---|
| Convex hull area | 541.5 | 642.4 (1.19x) |
| Mean pairwise distance | 19.03 | 21.02 |
| LOS/NLOS silhouette | 0.396 | 0.556 |
| Grid cells occupied (of 225) | 18 | 18 |

Each set reaches 7 grid cells that the other does not.

The UMAP projection uses the `umap-learn` package, which is included in `requirements.txt`.
