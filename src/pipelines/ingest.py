"""
ingest.py – Data Ingestion Pipeline Step
-----------------------------------------
WHY THIS EXISTS:
  In a notebook everything is in one place — loading, cleaning, training
  all mixed together. That makes it impossible to automate or test individually.
  By splitting into separate pipeline steps, each step can be versioned,
  tested, and triggered independently.

WHAT IT DOES:
  Loads the raw CSV from disk and splits it into train/test sets,
  saving both to the data/ folder for the next step (clean.py) to consume.
"""

import yaml
import pandas as pd
from sklearn.model_selection import train_test_split


class Ingestion:
    def __init__(self, config_path: str = "config.yml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def load_data(self):
        """Load raw CSV and split into train/test sets."""
        print("Loading data...")
        raw_path = self.config["data"]["raw_path"]
        df = pd.read_csv(raw_path)

        test_size = self.config["data"]["test_size"]
        random_state = self.config["data"]["random_state"]

        train, test = train_test_split(df, test_size=test_size, random_state=random_state)

        # Persist splits so other pipeline steps can consume them
        train.to_csv(self.config["data"]["train_path"], index=False)
        test.to_csv(self.config["data"]["test_path"], index=False)

        print(f"  Train size: {len(train)} rows, Test size: {len(test)} rows")
        return train, test
