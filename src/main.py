"""
main.py – Training Orchestrator with MLflow Tracking
------------------------------------------------------
WHY THIS EXISTS:
  In a notebook you run cells manually, in whatever order you remember.
  This orchestrator runs the full pipeline in one command: ingest →
  clean → train → evaluate. That makes it automatable — GitHub Actions
  calls `python main.py` and the whole thing runs unattended.

MLflow is integrated here so every training run automatically logs:
  - Parameters (n_estimators, max_depth, etc.)
  - Metrics (accuracy, ROC-AUC, precision, recall)
  - The trained model artifact
  - A registered model entry so versions are tracked over time

WHY MLFLOW:
  Without experiment tracking you have no idea which hyperparameters
  produced which accuracy score. MLflow solves this: every run is
  recorded, comparable side-by-side, and the best model can be
  promoted to production from the registry.
"""

import yaml
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

from pipelines.ingest import Ingestion
from pipelines.clean import Cleaner
from pipelines.train import Trainer


def main():
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    # ── 1. Set the MLflow experiment (creates it if it doesn't exist) ──
    mlflow.set_experiment("Insurance Claim Prediction")

    with mlflow.start_run() as run:
        print(f"\nMLflow run ID: {run.info.run_id}")

        # ── 2. Ingest ──────────────────────────────────────────────────
        ingestion = Ingestion()
        train_df, test_df = ingestion.load_data()

        # ── 3. Clean ───────────────────────────────────────────────────
        cleaner = Cleaner()
        train_clean = cleaner.clean_data(train_df)
        test_clean  = cleaner.clean_data(test_df)

        # ── 4. Train ───────────────────────────────────────────────────
        trainer = Trainer()
        X_train, y_train = trainer.feature_target_separator(train_clean)
        X_test,  y_test  = trainer.feature_target_separator(test_clean)
        trainer.train_model(X_train, y_train)
        trainer.save_model()

        # ── 5. Evaluate ────────────────────────────────────────────────
        y_pred   = trainer.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        roc      = roc_auc_score(y_test, y_pred)
        report   = classification_report(y_test, y_pred, output_dict=True)

        print(f"\n  Accuracy : {accuracy:.4f}")
        print(f"  ROC-AUC  : {roc:.4f}")

        # ── 6. Log params & metrics to MLflow ─────────────────────────
        mlflow.log_params(config["model"]["params"])
        mlflow.log_metric("accuracy",  accuracy)
        mlflow.log_metric("roc_auc",   roc)
        mlflow.log_metric("precision", report["weighted avg"]["precision"])
        mlflow.log_metric("recall",    report["weighted avg"]["recall"])

        # ── 7. Log the model artifact ──────────────────────────────────
        signature = mlflow.models.infer_signature(
            model_input=X_train,
            model_output=trainer.pipeline.predict(X_test),
        )
        mlflow.sklearn.log_model(
            trainer.pipeline,
            artifact_path="model",
            signature=signature,
        )

        # ── 8. Register the model so it appears in the Model Registry ──
        model_uri  = f"runs:/{run.info.run_id}/model"
        model_name = "insurance_claim_model"
        mlflow.register_model(model_uri, model_name)
        print(f"\n  Registered model: {model_name}")
        print("  Open 'mlflow ui' to compare runs in the dashboard.")


if __name__ == "__main__":
    main()
