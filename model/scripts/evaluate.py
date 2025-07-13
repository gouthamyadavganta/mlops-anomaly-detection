import pandas as pd
import mlflow.sklearn
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv("model/data/creditcard.csv")
X = df.drop("Class", axis=1)
y = df["Class"]

# Split test data
_, X_test, _, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Load latest model from mlruns
logged_model_uri = "runs:/d537b4a2dcb74e8aa4ab9ad0b1aae000/model"
model = mlflow.sklearn.load_model(logged_model_uri)

# Predict
y_pred = model.predict(X_test)
y_pred = [0 if p == 1 else 1 for p in y_pred]

# Report
report = classification_report(y_test, y_pred)
print("📊 Evaluation report:\n")
print(report)

