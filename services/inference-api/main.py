# services/inference/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/predict")
def predict(data: InputData):
    try:
        X = np.array(data.features).reshape(1, -1)
        prediction = model.predict(X)[0]
        return {"prediction": int(prediction)}  # -1 for anomaly, 1 for normal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# test trigger
