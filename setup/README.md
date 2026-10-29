# Data Capture

| Script | What it does |
|---|---|
| `capture.py` | parses a PuTTY serial log from the DWM1001 and writes one CSV row per capture |
| `combine.py` | merges raw per-channel files from `dataset/channels` into one CSV and adds `Label` and `Source_File` |

## Hardware

Two Decawave DWM1001 modules, one as initiator and one as responder, doing single-sided two-way ranging at 6.8 Mbps with a 64 MHz PRF on channels 1, 2, 3, 4, 5 and 7. The 1016-sample complex CIR is read from the accumulator (register 0x25) and its magnitude is approximated with the alpha-max-plus-beta-min method. Each channel's antenna delay was calibrated against a CONDTROL Traccer 30 laser distance meter at 2 m, which brings the residual LOS bias within 5 cm (see `eda.ipynb`). The DWM1001 firmware is not part of this repository; it is based on Decawave's [dwm1001-examples](https://github.com/Decawave/dwm1001-examples).

## Log format

The firmware prints one line per capture on the serial port:

```
DATA|distance|fp_index|fp_ampl1|fp_ampl2|fp_ampl3|rxpacc|std_noise|max_noise|cir0|cir1|...|cir1015|
```

`capture.py` ignores all other lines and skips captures with fewer than 1000 CIR values.

## Usage

```
python capture.py putty.log 16.09m_nlos_c5.csv
python combine.py combined_raw.csv 8.41m_los 9.29m_los 9.76m_los 9.54m_nlos 16.09m_nlos 16.80m_nlos
```

`combine.py` only reads files named `<distance>m_<los|nlos>_c<channel>.csv` and writes `combined_raw.csv` in `dataset/channels` by default, so the provided datasets are never overwritten. Without scenario arguments it merges every scenario in the folder. The ground-truth columns of the provided datasets are added afterwards in `eda.ipynb`.
