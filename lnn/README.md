# PL-MIND Encoder

The dual-circuit liquid neural network of the paper, with its Stage 2 and Stage 3 models. In the code the encoder is `DualCircuit_PI_HLNN`, built from two `PILiquidCell` circuits.

## Notebooks

In order:

| Notebook | Purpose |
|---|---|
| `stage1_pi_hlnn.ipynb` | trains the Stage 1 encoder and saves `stage1_pi_hlnn_best.pt` and `stage1_pi_hlnn_config.pt` |
| `stage1_unseen_test.ipynb` | tests it on the unseen environments |
| `stage2_bounce_classifier.ipynb` | Stage 2 single-bounce classifier; saves the embeddings used for Table II |
| `stage3_distance_pred.ipynb` | Stage 3 bounce distance prediction (Fig. 7) |
| `test_pipeline.ipynb` | runs all three stages on the test split |
| `tau_dynamics_learned.ipynb` | the x(t) → S(t) → τ(t) plot of Fig. 8, from a single simulated circuit with fixed parameters (`LRN`) |
| `data_preprocessing_visualization.ipynb` | plots the CIR preprocessing steps |

## Model

The input is the 60-sample CIR window from 10 samples before to 50 after the leading edge (searched in CIR indices 740 to 810), divided by RXPACC and scaled to [0, 1]. Two circuits of 32 neurons read it, and their hidden states are averaged over time into the 64-dim embedding.

| Paper | Code |
|---|---|
| Eq. 2: S(t) = Σ w_j σ_j | weights `coupling_w`; sigmoid gates on the circuit state with `activation_center` and `activation_width` |
| Eq. 3: τ = 1 / S(t) | τ = k / (λ + S(t)) with k = `smoothing` and λ = `signal_decay`; k = 1, λ = 0 gives Eq. 3 |
| Eq. 4: dh/dt = −h / τ + f(Wx + Uh) | k dv/dt = −λ(v − v₀) − S(t)(v − v_target) + I(x), i.e. dv/dt = −v / τ + (λv₀ + S(t) v_target + I(x)) / k, with v₀ = `noise_floor`, v_target = `signal_target` and the input gate I(x) from `input_coupling_w`, `input_center`, `input_width` |
| Eq. 5: Euler step, dt = 1 | 6 semi-implicit Euler sub-steps per sample, v kept in [−1, 1] |
| Eqs. 6–7: h + σ(Gate) · W_p h̃ | W_g = `gate_los`, `gate_nlos` and W_p = `P_nlos2los`, `P_los2nlos`, with Gate = W_g [h, W_p h̃], applied before each ODE step |
| Eq. 10: ∂τ/∂S < 0 | holds, since k and λ are positive |

Training: BCE plus the τ separation loss (weight 0.1, margin 0.1), AdamW (lr 1e-3, weight decay 1e-4), batch size 64 (the paper lists 60), dropout 0.2, gradient clipping 1.0, cosine schedule with a 3-epoch warmup, up to 50 epochs with early stopping on validation accuracy (patience 10), 70/15/15 stratified split, seed 42. 16,897 parameters.

## Stage 2 and Stage 3

- Stage 2: an NLOS sample is single-bounce when the largest amplitude within 3 samples of `bounce_path_idx` is at least half the largest amplitude from 5 samples before to 120 after the leading edge, and that range has at most 2 peaks (prominence 0.2, distance 5). A 200-tree random forest with balanced class weights learns this label from the embedding (70/30 split).
- Stage 3: a 200-tree random forest predicts `bounce_path_idx = fp_idx + (d_bounce - d_hardware) / 0.3003` (Eq. 1) from the embedding, `fp_idx` and `d_hardware` (Eq. 8), and `d_bounce = d_hardware + (predicted_idx - fp_idx) * 0.3003` (Eq. 9). It is trained on 70% of the single-bounce samples (9.54 m and 16.09 m).
