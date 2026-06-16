"""
train.py – Model Training Pipeline Step
-----------------------------------------
WHY THIS EXISTS:
  Training is isolated so it can be re-triggered automatically whenever
  new data arrives (Continuous Training). The model is saved to disk so
  it can be loaded by the prediction service (app.py) without retraining.

WHAT IT DOES:
  Separates features from target, trains a Random Forest classifier,
  wraps it in a sklearn Pipeline (handles column ordering), and saves
  the trained pipeline as a .pkl file.
"""

import yaml
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class Trainer:
    def __init__(self, config_path: str = "config.yml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.pipeline = None

    def feature_target_separator(self, df: pd.DataFrame):
        """Split a DataFrame into feature matrix X and target vector y."""
        target = self.config["model"]["target_column"]
        X = df.drop(columns=[target])
        y = df[target]
        return X, y

    def train_model(self, X_train, y_train):
        """Build and fit the sklearn pipeline."""
        print("Training model...")
        params = self.config["model"]["params"]

        self.pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth=params["max_depth"],
                random_state=params["random_state"],
            )),
        ])

        self.pipeline.fit(X_train, y_train)
        print("  Model training complete.")
        return self.pipeline

    def save_model(self):
        """Persist the trained pipeline to disk."""
        model_path = self.config["model"]["model_path"]
        joblib.dump(self.pipeline, model_path)
        print(f"  Model saved to {model_path}")
