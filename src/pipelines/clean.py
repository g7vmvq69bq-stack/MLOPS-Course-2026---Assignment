"""
clean.py – Data Cleaning Pipeline Step
----------------------------------------
WHY THIS EXISTS:
  Real-world data is messy — missing values, wrong types, duplicates.
  Cleaning is separated from ingestion so it can be unit-tested and
  swapped out without touching the rest of the pipeline.

WHAT IT DOES:
  Drops duplicates and rows with missing values, then ensures numeric
  columns have the correct dtype.
"""

import yaml
import pandas as pd


class Cleaner:
    def __init__(self, config_path: str = "config.yml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicates, nulls and fix dtypes."""
        print("Cleaning data...")
        initial_rows = len(df)

        df = df.drop_duplicates()
        df = df.dropna()

        # Ensure all columns except the target are numeric where possible
        target = self.config["model"]["target_column"]
        for col in df.columns:
            if col != target:
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass  # leave non-numeric columns as-is

        print(f"  Removed {initial_rows - len(df)} bad rows, {len(df)} remain")
        return df.reset_index(drop=True)
