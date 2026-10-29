# 1D-CNN Baseline

One of the three baselines in the paper (Tables I and II). Three Conv1d blocks with batch norm and ReLU (16, 32 and 128 channels; kernels 5, 5 and 3; the last two with stride 2) and global average pooling give a 128-dim embedding, followed by Linear(128, 32) → SiLU → Dropout(0.4) → Linear(32, 1) → Sigmoid. 19,617 parameters.

Training uses BCE and otherwise the same settings as PL-MIND (see [../lnn/README.md](../lnn/README.md#model)), except for the dropout of 0.4.

## Notebooks

In order:

| Notebook | Purpose |
|---|---|
| `stage1_cnn.ipynb` | trains the Stage 1 model and saves `stage1_cnn_best.pt` and `stage1_cnn_config.pt` |
| `stage1_unseen_test.ipynb` | tests it on the unseen environments |
| `stage2_bounce_classifier.ipynb` | Stage 2 random forest on the frozen embedding; saves the embeddings used for Table II |
