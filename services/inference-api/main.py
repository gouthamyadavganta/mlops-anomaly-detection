from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import joblib
import numpy as np
import os

app = FastAPI()

# Load model on startup
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Input schema
class InputData(BaseModel):
    features: list[float]

# Prometheus metrics
inference_requests = Counter("inference_requests_total", "Total number of inference requests")
anomaly_predictions = Counter("anomaly_predictions_total", "Total number of anomalies predicted")
drift_alerts = Counter("drift_alerts_total", "Total number of drift alerts")

# Drift detection (rolling average)
DRIFT_THRESHOLD = 0.3
rolling_preds = []

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/predict")
def predict(data: InputData):
    inference_requests.inc()

    try:
        X = np.array(data.features).reshape(1, -1)
        prediction = model.predict(X)[0]

        # Anomaly = -1
        if prediction == -1:
            anomaly_predictions.inc()

        # Drift detection logic
        rolling_preds.append(1 if prediction == -1 else 0)
        if len(rolling_preds) > 20:
            rolling_preds.pop(0)
        drift_score = sum(rolling_preds) / len(rolling_preds)
        if drift_score > DRIFT_THRESHOLD:
            drift_alerts.inc()

        return {"prediction": int(prediction), "drift_score": round(drift_score, 3)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

