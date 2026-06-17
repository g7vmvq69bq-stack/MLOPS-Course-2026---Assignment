# MLOps Course 2026 – Final Assignment

A production-ready MLOps pipeline built across four classes, evolving from a local
notebook experiment to a fully automated, containerised, cloud-deployed machine
learning system.

## MLOps Maturity Progression

| Phase | Class | What was added | Maturity level |
|-------|-------|----------------|----------------|
| 1 | Class 1 | Local Terraform S3 bucket | Level 0 |
| 2 | Class 2 | Remote backend, Terraform modules, GitHub Actions CI/CD | Level 1 |
| 3 | Class 3 | ML pipelines, DVC data versioning, FastAPI, Docker | Level 1 → 2 |
| 4 | Class 4 | ECR, ECS Fargate deployment, MLflow, manual approval gate | Level 2 + CT |
| Bonus | Extra | Multi-model comparison, Evidently AI monitoring, Model Registry | Level 2 + CT + CM |

## Tools & Concepts

| Concept | Tool | Why |
|---------|------|-----|
| Infrastructure as Code | Terraform | Reproducible, reviewable cloud infrastructure |
| Remote state management | S3 backend + state lock | Safe collaboration on infra across developers |
| Code versioning | Git + GitHub | Track every change; feature-branch workflow |
| CI/CD | GitHub Actions | Automate plan/apply; fail fast on bad code |
| Manual approval gate | trstringer/manual-approval | Four-eyes principle before infra changes reach prod |
| Data versioning | DVC | Link each model version to the exact data it was trained on |
| Model serving | FastAPI + uvicorn | Expose predictions as a REST API |
| Containerisation | Docker | Same image runs locally, in CI, and in the cloud |
| Container registry | AWS ECR | Versioned Docker images ready for cloud deployment |
| Cloud deployment | AWS ECS Fargate | Serverless container hosting; no server management |
| Experiment tracking | MLflow | Compare runs, log metrics/params, register models |
| Model Registry | MLflow Model Registry | Version and govern every model promoted to production |
| Multi-model comparison | MLflow + scikit-learn | Train RF, GBM, LR — auto-select best by ROC-AUC |
| Continuous Training | App CI/CD (DVC → retrain → ECR push) | Fresh model deployed automatically on code/data change |
| Continuous Monitoring | Evidently AI | Auto-detect data drift after every training run; HTML report saved to reports/ |

## Repository Structure

```
mlops-course-2026/
├── terraform/                  # Infrastructure as Code (Phases 1–4)
│   ├── backends/               # One .conf per environment
│   ├── environments/           # One .tfvars per environment
│   ├── modules/
│   │   ├── s3-bucket/          # Reusable S3 module
│   │   ├── ecr-repository/     # Reusable ECR module
│   │   └── ecs-fargate-service/# Reusable ECS Fargate module
│   ├── provider.tf
│   ├── variables.tf
│   ├── s3_buckets.tf
│   └── ecr_repositories.tf
├── src/                        # ML application (Phases 3–4)
│   ├── pipelines/
│   │   ├── ingest.py           # Load raw CSV, split train/test
│   │   ├── clean.py            # Remove nulls and duplicates
│   │   ├── train.py            # StandardScaler + RandomForest pipeline
│   │   └── predict.py          # Load model and run inference
│   ├── data/                   # Tracked by DVC, NOT Git
│   ├── models/                 # Generated at training time
│   ├── reports/                # Evidently AI HTML drift reports (generated, NOT Git)
│   ├── app.py                  # FastAPI prediction service
│   ├── main.py                 # Multi-model orchestrator + MLflow + Evidently
│   ├── config.yml              # Centralised configuration
│   ├── requirements.txt
│   └── Dockerfile
└── .github/
    └── workflows/
        ├── tf-infra-cicd-dev.yml   # Infrastructure CI/CD
        └── app-cicd-dev.yml        # Application CI/CD (CT)
```

## Reference
Course repository: https://github.com/geekzyn/mlops-course-2025
