"""
predict.py – Prediction Pipeline Step
---------------------------------------
WHY THIS EXISTS:
  Separating prediction from training means the model can be swapped
  (updated pkl file) without changing any serving code. The FastAPI
  app (app.py) delegates to this class.

WHAT IT DOES:
  Loads a saved sklearn pipeline from disk and runs inference on
  new input data supplied as a pandas DataFrame.
"""

import joblib
import pandas as pd


class Predictor:
    def __init__(self, model_path: str = "models/model.pkl"):
        self.model = joblib.load(model_path)

    def predict(self, input_df: pd.DataFrame):
        """Run the model on a DataFrame and return predictions."""
        predictions = self.model.predict(input_df)
        return predictions.tolist()
