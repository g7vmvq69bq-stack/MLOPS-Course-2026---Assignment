"""
app.py – FastAPI Prediction Service
-------------------------------------
WHY FASTAPI:
  The trained model sitting in a .pkl file is useless unless something
  can call it. FastAPI turns the model into a web service that any
  application — a website, a mobile app, another microservice — can
  call over HTTP by sending JSON and getting a prediction back.

TWO ENDPOINTS:
  GET  /         → health check (is the service alive?)
  POST /predict  → accepts patient data as JSON, returns 0 or 1
                   (0 = no insurance claim, 1 = claim predicted)

WHY A HEALTH CHECK:
  In production, load balancers and orchestrators (ECS, Kubernetes)
  call the health endpoint every few seconds. If it stops returning 200,
  the platform knows the container is dead and restarts it automatically.
"""

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Insurance Claim Prediction API",
    description="MLOps Course 2026 — Phase 3/4 model serving layer",
    version="1.0.0",
)

# Load the trained model once at startup (not on every request)
try:
    model = joblib.load("models/model.pkl")
except FileNotFoundError:
    model = None  # Will raise a clear error on /predict if not found


# ── Request schema ─────────────────────────────────────────────────────────────
class InputData(BaseModel):
    age: float
    sex: float
    bmi: float
    children: float
    smoker: float
    region: float

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "sex": 1,
                "bmi": 27.5,
                "children": 2,
                "smoker": 0,
                "region": 1,
            }
        }


# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.get("/")
def health_check():
    """Health check endpoint — called by load balancers and ECS to verify the
    container is running and the model is loaded."""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "service": "insurance-claim-prediction",
    }


@app.post("/predict")
def predict(data: InputData):
    """Predict whether a patient will make an insurance claim.

    Returns:
        prediction: 0 (no claim) or 1 (claim predicted)
        probability: confidence score for the positive class
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run main.py to train the model first.",
        )

    input_df = pd.DataFrame([data.model_dump()])
    prediction  = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "label": "claim predicted" if prediction == 1 else "no claim",
    }
