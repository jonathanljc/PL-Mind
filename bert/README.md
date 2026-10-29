# BERT-style Transformer Baseline

One of the three baselines in the paper (Tables I and II). Each of the 60 CIR samples is projected to 64 dimensions and given a learned positional embedding, followed by two Transformer encoder layers (4 attention heads, feed-forward size 128). The hidden states are averaged over the 60 positions and normalised with LayerNorm (there is no CLS token), followed by Linear(64, 32) → SiLU → Dropout(0.2) → Linear(32, 1) → Sigmoid. 73,153 parameters.

Training uses BCE and otherwise the same settings as PL-MIND (see [../lnn/README.md](../lnn/README.md#model)), except for at most 40 epochs.

## Notebooks

In order:

| Notebook | Purpose |
|---|---|
| `stage1_bert.ipynb` | trains the Stage 1 model and saves `stage1_bert_best.pt` and `stage1_bert_config.pt` |
| `stage1_unseen_test.ipynb` | tests it on the unseen environments |
| `stage2_bounce_classifier.ipynb` | Stage 2 random forest on the frozen embedding; saves the embeddings used for Table II |
