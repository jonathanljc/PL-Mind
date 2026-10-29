# LSTM Baseline

One of the three baselines in the paper (Tables I and II). One LSTM layer with 64 hidden units reads the 60-sample CIR window from zero initial states; the hidden states are averaged over time into a 64-dim embedding, followed by Linear(64, 32) → SiLU → Dropout(0.2) → Linear(32, 1) → Sigmoid. 19,265 parameters.

Training uses BCE and otherwise the same settings as PL-MIND (see [../lnn/README.md](../lnn/README.md#model)).

## Notebooks

In order:

| Notebook | Purpose |
|---|---|
| `stage1_lstm.ipynb` | trains the Stage 1 model and saves `stage1_lstm_best.pt` and `stage1_lstm_config.pt` |
| `stage1_unseen_test.ipynb` | tests it on the unseen environments |
| `stage2_bounce_classifier.ipynb` | Stage 2 random forest on the frozen embedding; saves the embeddings used for Table II |
