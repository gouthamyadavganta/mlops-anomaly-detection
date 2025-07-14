import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
import urllib.request
import boto3
import botocore
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# === Config ===
USE_REMOTE_TRACKING = False  # Set to True when MLflow server is deployed
MLFLOW_TRACKING_URI = "http://<MLFLOW_SERVER_IP>:5000"  # To be updated later
S3_BUCKET_NAME = "mlops-anomaly-dev-mlflow-artifacts"
MODEL_FILENAME = "model.pkl"
DATA_PATH = "../data/creditcard.csv"

# === Ensure dataset exists ===
if not os.path.exists(DATA_PATH):
    print("📥 Dataset not found, downloading...")
    os.makedirs("../data", exist_ok=True)
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv",
        DATA_PATH
    )
    print("✅ Dataset downloaded.")

# === Load dataset ===
df = pd.read_csv(DATA_PATH)
X = df.drop("Class", axis=1)
y = df["Class"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# === Setup MLflow ===
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI if USE_REMOTE_TRACKING else "file:./mlruns")
mlflow.set_experiment("Anomaly-Detection")

model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

with mlflow.start_run():
    model.fit(X_train)
    joblib.dump(model, MODEL_FILENAME)

    # Predict and evaluate
    y_pred = model.predict(X_test)
    y_pred = [0 if p == 1 else 1 for p in y_pred]
    report = classification_report(y_test, y_pred, output_dict=True)

    # Log to MLflow
    mlflow.log_params({
        "model": "IsolationForest",
        "contamination": 0.01
    })

    mlflow.log_metrics({
        "precision": report["1"]["precision"],
        "recall": report["1"]["recall"],
        "f1-score": report["1"]["f1-score"]
    })

    mlflow.sklearn.log_model(model, "model")
    print("✅ Model trained and logged to MLflow.")

# === Optional S3 Upload ===
if USE_REMOTE_TRACKING:
    try:
        print("🚀 Uploading model to S3...")
        s3_client = boto3.client("s3")
        s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
        s3_client.upload_file(MODEL_FILENAME, S3_BUCKET_NAME, f"models/{MODEL_FILENAME}")
        print(f"✅ model.pkl uploaded to s3://{S3_BUCKET_NAME}/models/{MODEL_FILENAME}")
    except botocore.exceptions.ClientError as e:
        print(f"⚠️ Skipping S3 upload: {e.response['Error']['Message']}")

