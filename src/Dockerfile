# ── WHY DOCKER ────────────────────────────────────────────────────────────────
# Without Docker, "it works on my laptop" is a constant problem.
# Docker packages the Python interpreter, all libraries, the trained model,
# and the FastAPI app into one self-contained image.
# That image runs identically on your Mac, on a colleague's Windows machine,
# in GitHub Actions, and on AWS ECS Fargate — zero environment differences.
# ─────────────────────────────────────────────────────────────────────────────

# Start from the official slim Python image (smaller = faster to pull in cloud)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# ── Install dependencies FIRST (Docker layer caching) ────────────────────────
# Copying requirements.txt before the rest of the code means Docker only
# re-runs pip install when requirements change, not on every code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy the rest of the application code ────────────────────────────────────
COPY . .

# The port FastAPI / uvicorn listens on inside the container
EXPOSE 80

# ── Start the FastAPI server ──────────────────────────────────────────────────
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
