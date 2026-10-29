# Dataset

UWB channel impulse response (CIR) captures from two Decawave DWM1001 modules (single-sided two-way ranging, 6.8 Mbps, 64 MHz PRF). Each capture holds the distance reported by the DW1000, its first-path registers and the 1016-sample CIR magnitude.

## Folders

| Folder | Contents |
|---|---|
| `channels/` | one file per scenario and channel (100 captures each), plus the combined datasets that the notebooks use |
| `calibrations/` | 20 LOS captures at 2 m for each channel, used in `eda.ipynb` to check the antenna delay calibration |

## Scenarios

Every scenario was recorded on channels 1, 2, 3, 4, 5 and 7, so it has 600 captures.

| Scenario | Condition | Set | Location | d_direct (m) | d_bounce (m) |
|---|---|---|---|---|---|
| 8.41m | LOS | ID | SIT E2-B2, concrete / glossy wall | 8.41 | - |
| 9.29m | LOS | ID | SIT E2-B2, concrete / glass wall | 9.29 | - |
| 9.76m | LOS | ID | SIT E2-L9, concrete wall | 9.76 | - |
| 9.54m | NLOS | ID | SIT E2-B2, concrete / glass wall | 7.668 | 9.54 |
| 16.09m | NLOS | ID | SIT E2-B2, concrete / glossy wall | 7.20139 | 16.09 |
| 16.80m | NLOS | ID | SIT E2-L9, concrete wall | 13.05986 | 16.80 |
| 4.55m | LOS | OOD | HDB flat or SIT E2-L1 corridor | 4.55 | - |
| 10.19m | LOS | OOD | HDB flat or SIT E2-L1 corridor | 10.19 | - |
| 8.91m | NLOS | OOD | SIT E2-L1 corridor | 6.10 | 8.91 |
| 12.79m | NLOS | OOD | HDB flat (the path crosses three rooms) | 8.81887 | 12.79 |

ID scenarios are used for training, validation and the in-distribution test; OOD scenarios only for testing. The OOD set has one LOS and one NLOS scenario in each of its two places. For LOS the scenario name is the laser-measured TX to RX distance. For NLOS it is the laser-measured TX to reflector to RX length (`d_bounce`), and `d_direct` is the straight TX to RX distance from the floor plan.

## Files in `channels/`

| File | Rows | Contents |
|---|---|---|
| `<distance>m_<los\|nlos>_c<channel>.csv` | 100 | raw captures of one scenario on one channel, e.g. `16.09m_nlos_c5.csv` |
| `combined_uwb_dataset.csv` | 3600 | the six ID scenarios on all six channels, with labels |
| `unseen_dataset.csv` | 2400 | the four OOD scenarios on all six channels, with labels |
| `single_channel5_dataset.csv` | 600 | channel 5 only, 100 captures for each of 6 scenarios |
| `multi_channel4_dataset.csv` | 600 | channels 1, 3, 4 and 7, 25 captures per channel for each of 6 scenarios (adds a `scenario` column) |

The single- and multi-channel subsets share four scenarios; see `multichannel/README.md`.

## Columns

Raw capture files (written by `setup/capture.py`):

| Column | Meaning |
|---|---|
| `Capture_ID` | capture number within the recording |
| `Distance` | distance reported by the DW1000 (m), `d_hardware` in the notebooks |
| `FP_INDEX` | first-path index register; `FP_INDEX / 64` is the CIR index of the detected first path |
| `FP_AMPL1`, `FP_AMPL2`, `FP_AMPL3` | first-path amplitude registers |
| `RXPACC` | preamble accumulation count, used to normalise the CIR |
| `STD_NOISE`, `MAX_NOISE` | noise statistics reported by the DW1000 |
| `CIR0` ... `CIR1015` | CIR magnitude |

Extra columns in the combined files:

| Column | Meaning |
|---|---|
| `Label` | 0 = LOS, 1 = NLOS |
| `Source_File` | raw file the row came from |
| `d_direct`, `d_bounce` | ground-truth distances in metres (`d_bounce` is empty for LOS) |
| `fp_idx` | `FP_INDEX / 64` |
| `los_path_idx`, `bounce_path_idx` | CIR index of the direct and of the single-bounce path, `fp_idx + (d - Distance) / 0.3002` |
| `fp_to_los_offset` | `fp_idx - los_path_idx`, how far the hardware first path is from the direct path |
| `peak_idx` | CIR index of the strongest sample |
| `channel` | UWB channel (not in `single_channel5_dataset.csv`, which is channel 5 only) |
| `cir_at_los_path` | CIR value at `los_path_idx` |
| `num_peaks`, `bounce_dominance`, `is_correctable` | Stage 2 labels; `is_correctable` is 1 for NLOS samples with bounce dominance of at least 0.5 and at most 2 peaks, otherwise 0 (only in `combined_uwb_dataset.csv` and `unseen_dataset.csv`) |

One CIR index is c x 1.0016 ns = 0.3003 m (d_sample in Eq. 1 of the paper). The path-index columns were computed with 0.3002 m in `eda.ipynb` and Stage 3 uses 0.3003 m; over these distances the two differ by less than 0.01 samples.

## How the files were made

1. `setup/capture.py` converts the serial log of each recording into one raw file.
2. The raw files were merged and labelled (`setup/combine.py` does the merge).
3. `eda.ipynb` computes the ground-truth columns (`d_direct`, `d_bounce`, `fp_idx`, the path indices and the rest). Its export cell writes them for all ten scenarios to `channels/eda_labeled_export.csv`, so the provided files are left as they are.

The combined files in `channels/` are the ones used for the paper, and every raw file matches its rows in `combined_uwb_dataset.csv` or `unseen_dataset.csv` exactly. `9.29m_los_c2.csv` was rebuilt from those rows because the raw file in the folder held a different recording (mean reported distance 9.77 m instead of about 9.35 m).
