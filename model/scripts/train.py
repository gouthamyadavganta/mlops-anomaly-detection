import os

# ✅ Set AWS + S3 endpoint configs
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://s3.us-east-2.amazonaws.com"
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY", "")
os.environ["AWS_REGION"] = "us-east-2"
os.environ["AWS_DEFAULT_REGION"] = "us-east-2"

print("✅ MLFLOW_S3_ENDPOINT_URL:", os.environ.get("MLFLOW_S3_ENDPOINT_URL"))
print("✅ AWS_DEFAULT_REGION:", os.environ.get("AWS_DEFAULT_REGION"))

import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
import urllib.request
import boto3
import botocore
from mlflow.tracking import MlflowClient
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# === Config ===
USE_REMOTE_TRACKING = True
MLFLOW_TRACKING_URI = "http://aef27c7c07e634833bf412c822a538fe-2121813122.us-east-2.elb.amazonaws.com:5000"
S3_BUCKET_NAME = "mlops-anomaly-dev-mlflow-artifacts"
MODEL_FILENAME = "model.pkl"
DATA_PATH = "../data/creditcard.csv"

print("📍 MLflow tracking URI:", MLFLOW_TRACKING_URI)

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

# === Setup MLflow tracking ===
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI if USE_REMOTE_TRACKING else "file:./mlruns")
client = MlflowClient()
experiment_name = "Anomaly-Detection"
artifact_path = f"s3://{S3_BUCKET_NAME}"  # ✅ no /mlflow-artifacts

try:
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = client.create_experiment(
            name=experiment_name,
            artifact_location=artifact_path
        )
    else:
        experiment_id = experiment.experiment_id
except Exception as e:
    print("⚠️ Failed to get or create experiment:", e)
    raise

# === Train and log model ===
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

with mlflow.start_run(experiment_id=experiment_id) as run:
    model.fit(X_train)
    import uuid
    model._retrain_id = str(uuid.uuid4())

    joblib.dump(model, MODEL_FILENAME)

    y_pred = model.predict(X_test)
    y_pred = [0 if p == 1 else 1 for p in y_pred]
    report = classification_report(y_test, y_pred, output_dict=True)

    mlflow.log_params({
        "model": "IsolationForest",
        "contamination": 0.01
    })

    mlflow.log_metrics({
        "precision": report["1"]["precision"],
        "recall": report["1"]["recall"],
        "f1-score": report["1"]["f1-score"]
    })

    mlflow.log_artifact(MODEL_FILENAME)
    print(f"✅ Model trained and logged to MLflow.")
    print(f"🏃 View run {run.info.run_name} at: {MLFLOW_TRACKING_URI}/#/experiments/{experiment_id}/runs/{run.info.run_id}")
    print(f"🧪 View experiment at: {MLFLOW_TRACKING_URI}/#/experiments/{experiment_id}")

# === Optional S3 upload (separate) ===
if USE_REMOTE_TRACKING:
    try:
        print("🚀 Uploading model to S3 (manual backup)...")
        s3_client = boto3.client("s3", region_name="us-east-2", endpoint_url="https://s3.us-east-2.amazonaws.com")
        s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
        s3_client.upload_file(MODEL_FILENAME, S3_BUCKET_NAME, f"models/{MODEL_FILENAME}")
        print(f"✅ model.pkl uploaded to s3://{S3_BUCKET_NAME}/models/{MODEL_FILENAME}")
        print("✅ Triggered: Pipeline end-to-end tested and  working.")
    except botocore.exceptions.ClientError as e:
        print(f"⚠️ Skipping S3 upload: {e.response['Error']['Message']}")

# test trigger
