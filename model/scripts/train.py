import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import mlflow
import mlflow.sklearn
import joblib

# Load dataset
df = pd.read_csv("../data/creditcard.csv")
X = df.drop("Class", axis=1)
y = df["Class"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# Initialize model
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

# MLflow setup
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Anomaly-Detection")

with mlflow.start_run():
    # Fit model
    model.fit(X_train)

    # Save model locally
    joblib.dump(model, "model.pkl")

    # Predict and evaluate
    y_pred = model.predict(X_test)
    y_pred = [0 if p == 1 else 1 for p in y_pred]  # Convert ISOForest labels

    report = classification_report(y_test, y_pred, output_dict=True)

    # Log params and metrics
    mlflow.log_params({
        "model": "IsolationForest",
        "contamination": 0.01
    })

    mlflow.log_metrics({
        "precision": report['1']['precision'],
        "recall": report['1']['recall'],
        "f1-score": report['1']['f1-score']
    })

    # Log model to MLflow
    mlflow.sklearn.log_model(model, "model")

    print("✅ Model trained, saved to disk, and logged to MLflow.")

