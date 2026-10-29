"""Convert a PuTTY serial log from the DWM1001 into a CSV of CIR captures.

Every capture is one line in the log:
    DATA|distance|fp_index|fp_ampl1|fp_ampl2|fp_ampl3|rxpacc|std_noise|max_noise|cir0|cir1|...
The CIR values are magnitudes. Captures with fewer than 1000 CIR samples are skipped.

usage: python capture.py [putty.log] [output.csv]
"""
import sys

import pandas as pd

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else 'putty.log'
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else 'capture.csv'

print(f"Reading {LOG_FILE}...")

with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

all_data = []
capture_id = 0

for line in lines:
    if line.startswith('DATA|'):
        try:
            # drop the "DATA|" prefix and the trailing "|"
            parts = line[5:].strip().rstrip('|').split('|')
            if len(parts) < 8:
                continue

            row = {
                'Capture_ID': capture_id,
                'Distance': float(parts[0]),
                'FP_INDEX': int(parts[1]),
                'FP_AMPL1': int(parts[2]),
                'FP_AMPL2': int(parts[3]),
                'FP_AMPL3': int(parts[4]),
                'RXPACC': int(parts[5]),
                'STD_NOISE': int(parts[6]),
                'MAX_NOISE': int(parts[7]),
            }

            # the rest of the line is the CIR magnitude
            cir_start = 8
            sample_num = 0

            for val in parts[cir_start:]:
                try:
                    row[f'CIR{sample_num}'] = int(val)
                    sample_num += 1
                except ValueError:
                    pass  # skip corrupted values

            if sample_num >= 1000:
                all_data.append(row)
                print(f"Capture {capture_id}: {sample_num} CIR samples")
                capture_id += 1
            else:
                print(f"Capture {capture_id}: only {sample_num} samples, skipped")

        except Exception as e:
            print(f"Error: {e}")

if len(all_data) > 0:
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved {len(df)} captures to {OUTPUT_FILE}")
    print(f"Columns: {len(df.columns)} (9 metadata + {len(df.columns) - 9} CIR)")
    print(df.head())
else:
    print("\nNo valid data found")
