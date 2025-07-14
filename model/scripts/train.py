import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# CONFIG
USE_REMOTE_TRACKING = False
S3_BUCKET_NAME = "mlops-anomaly-dev-mlflow-artifacts"
MODEL_FILENAME = "model.pkl"

# MLflow Setup
if USE_REMOTE_TRACKING:
    mlflow.set_tracking_uri("http://<MLFLOW_SERVER_IP>:5000")  # TO BE SET LATER
else:
    mlflow.set_tracking_uri("file:./mlruns")

mlflow.set_experiment("Anomaly-Detection")

# Load Dataset
df = pd.read_csv("../data/creditcard.csv")
X = df.drop("Class", axis=1)
y = df["Class"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)

model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

with mlflow.start_run():
    model.fit(X_train)

    joblib.dump(model, MODEL_FILENAME)

    y_pred = model.predict(X_test)
    y_pred = [0 if p == 1 else 1 for p in y_pred]

    report = classification_report(y_test, y_pred, output_dict=True)

    mlflow.log_params({"model": "IsolationForest", "contamination": 0.01})
    mlflow.log_metrics({
        "precision": report["1"]["precision"],
        "recall": report["1"]["recall"],
        "f1-score": report["1"]["f1-score"]
    })

    mlflow.sklearn.log_model(model, "model")
    print("✅ Model trained and logged to MLflow.")

    # Upload to S3 (only if infra ready)
    if USE_REMOTE_TRACKING:
        import boto3
        s3 = boto3.client("s3")
        s3.upload_file(MODEL_FILENAME, S3_BUCKET_NAME, f"models/{MODEL_FILENAME}")
        print(f"✅ Uploaded to s3://{S3_BUCKET_NAME}/models/{MODEL_FILENAME}")

import botocore

# Upload model to S3 only if bucket exists
try:
    s3_client.head_bucket(Bucket=bucket_name)
    s3_client.upload_file("model.pkl", bucket_name, "models/model.pkl")
    print(f"✅ model.pkl uploaded to s3://{bucket_name}/models/model.pkl")
except botocore.exceptions.ClientError as e:
    print(f"⚠️ Skipping S3 upload: {e.response['Error']['Message']}")

