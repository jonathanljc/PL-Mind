"""Merge the per-channel capture files in dataset/channels into one labelled CSV.

Each raw file is named <distance>m_<los|nlos>_c<channel>.csv. The script adds a Label
column (0 = LOS, 1 = NLOS) and a Source_File column and concatenates the files. The
combined datasets already in the folder (combined_uwb_dataset.csv, unseen_dataset.csv, ...)
are never read or overwritten; the output goes to combined_raw.csv unless another name is given.

usage: python combine.py [output.csv] [scenario ...]
e.g.   python combine.py train_raw.csv 8.41m_los 9.29m_los 9.76m_los 9.54m_nlos 16.09m_nlos 16.80m_nlos
"""
import glob
import os
import re
import sys

import pandas as pd

CHANNEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dataset', 'channels')
RAW_FILE = re.compile(r'^(\d+(?:\.\d+)?m_(los|nlos))_c\d+\.csv$')


def combine_all_datasets(search_path=CHANNEL_DIR, output_name='combined_raw.csv', scenarios=None):
    """Label the raw per-channel files in search_path and save them as one CSV."""
    all_files = sorted(glob.glob(os.path.join(search_path, "*.csv")))
    raw_files = [f for f in all_files if RAW_FILE.match(os.path.basename(f).lower())]
    if scenarios:
        raw_files = [f for f in raw_files if RAW_FILE.match(os.path.basename(f).lower()).group(1) in scenarios]

    if not raw_files:
        print(f"No per-channel CSV files found in {search_path}")
        return None

    print(f"Found {len(raw_files)} files in {search_path}. Combining...")

    combined_data = []

    for filename in raw_files:
        try:
            fname = os.path.basename(filename).lower()
            is_nlos = RAW_FILE.match(fname).group(2) == 'nlos'
            label = 1 if is_nlos else 0
            label_str = "NLOS" if is_nlos else "LOS"

            df = pd.read_csv(filename)
            df['Label'] = label
            df['Source_File'] = fname

            # Label and Source_File first, then the capture columns
            cols = ['Label', 'Source_File'] + [c for c in df.columns if c not in ['Label', 'Source_File']]
            df = df[cols]

            combined_data.append(df)
            print(f"   Added {fname:<20} ({len(df)} samples) -> {label_str}")

        except Exception as e:
            print(f"   Error reading {filename}: {e}")

    if combined_data:
        master_df = pd.concat(combined_data, ignore_index=True)

        print(f"\nTotal samples: {len(master_df)}")
        print(f"Total columns: {len(master_df.columns)}")
        print("Label distribution:")
        print(master_df['Label'].value_counts())

        output_filename = os.path.join(search_path, output_name)
        master_df.to_csv(output_filename, index=False)
        print(f"Saved to {output_filename}")

        return master_df
    else:
        return None


if __name__ == '__main__':
    out_name = sys.argv[1] if len(sys.argv) > 1 else 'combined_raw.csv'
    df_combined = combine_all_datasets(output_name=out_name, scenarios=set(sys.argv[2:]) or None)
