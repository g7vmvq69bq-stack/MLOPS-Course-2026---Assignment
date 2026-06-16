"""
main.py – Multi-Model Training Orchestrator with MLflow Tracking
-----------------------------------------------------------------
BONUS CONCEPT: Train multiple models, compare them, promote the best one.

WHY THIS MATTERS:
  A single model run is a guess. Training multiple algorithms and comparing
  their metrics in MLflow lets us make an evidence-based decision about which
  model goes to production. This is the "Compare multiple models and pick the
  best" MLOps best practice.

WHAT IT DOES:
  1. Runs the ingest → clean pipeline once
  2. Trains 3 different models (Random Forest, Gradient Boosting, Logistic
     Regression) — each in its own MLflow run
  3. Compares their ROC-AUC scores
  4. Saves the best model to disk and registers it in the MLflow Model Registry
"""

import yaml
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

from pipelines.ingest import Ingestion
from pipelines.clean import Cleaner
from pipelines.train import Trainer


def train_and_log(model, model_name, X_train, y_train, X_test, y_test, config):
    """Train one model, log everything to MLflow, return the ROC-AUC score."""
    with mlflow.start_run(run_name=model_name) as run:
        # ── Train ──────────────────────────────────────────────────────────
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # ── Metrics ────────────────────────────────────────────────────────
        accuracy = accuracy_score(y_test, y_pred)
        roc      = roc_auc_score(y_test, y_pred)
        report   = classification_report(y_test, y_pred, output_dict=True)

        print(f"  {model_name:<30} accuracy={accuracy:.4f}  ROC-AUC={roc:.4f}")

        # ── Log to MLflow ──────────────────────────────────────────────────
        mlflow.log_param("model_type", model_name)
        mlflow.log_params(model.get_params())
        mlflow.log_metric("accuracy",  accuracy)
        mlflow.log_metric("roc_auc",   roc)
        mlflow.log_metric("precision", report["weighted avg"]["precision"])
        mlflow.log_metric("recall",    report["weighted avg"]["recall"])

        signature = mlflow.models.infer_signature(X_train, model.predict(X_test))
        mlflow.sklearn.log_model(model, artifact_path="model", signature=signature)

        return roc, model, run.info.run_id


def main():
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    # ── 1. Ingest & Clean ─────────────────────────────────────────────────
    ingestion = Ingestion()
    train_df, test_df = ingestion.load_data()

    cleaner = Cleaner()
    train_clean = cleaner.clean_data(train_df)
    test_clean  = cleaner.clean_data(test_df)

    trainer = Trainer()
    X_train, y_train = trainer.feature_target_separator(train_clean)
    X_test,  y_test  = trainer.feature_target_separator(test_clean)

    # ── 2. Define candidate models ────────────────────────────────────────
    params = config["model"]["params"]
    candidates = {
        "RandomForest": RandomForestClassifier(
            n_estimators    = params["n_estimators"],
            max_depth       = params["max_depth"],
            min_samples_split = params.get("min_samples_split", 5),
            random_state    = params["random_state"],
        ),
        "GradientBoosting": GradientBoostingClassifier(
            n_estimators  = params["n_estimators"],
            max_depth     = min(params["max_depth"], 5),
            random_state  = params["random_state"],
        ),
        "LogisticRegression": LogisticRegression(
            max_iter     = 1000,
            random_state = params["random_state"],
        ),
    }

    # ── 3. Train all models, track with MLflow ────────────────────────────
    mlflow.set_experiment("Insurance Claim Prediction")
    print("\nTraining and comparing models...")

    best_roc      = 0
    best_model    = None
    best_run_id   = None
    best_name     = None

    for name, model in candidates.items():
        roc, trained_model, run_id = train_and_log(
            model, name, X_train, y_train, X_test, y_test, config
        )
        if roc > best_roc:
            best_roc    = roc
            best_model  = trained_model
            best_run_id = run_id
            best_name   = name

    # ── 4. Save and register the BEST model ───────────────────────────────
    print(f"\n✅ Best model: {best_name} (ROC-AUC = {best_roc:.4f})")
    joblib.dump(best_model, config["model"]["model_path"])
    print(f"   Saved to {config['model']['model_path']}")

    model_uri  = f"runs:/{best_run_id}/model"
    model_name = "insurance_claim_model"
    mlflow.register_model(model_uri, model_name)
    print(f"   Registered as '{model_name}' in MLflow Model Registry")
    print("\n   Open 'mlflow ui' to compare all runs in the dashboard.")


if __name__ == "__main__":
    main()
