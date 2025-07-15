import json
import os
import subprocess

DRIFT_STATE_FILE = os.path.join(os.path.dirname(__file__), "drift_state.json")
TRAIN_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/train.py"))

def load_drift_state():
    if not os.path.exists(DRIFT_STATE_FILE):
        print("Drift state file not found.")
        return None

    with open(DRIFT_STATE_FILE, "r") as f:
        return json.load(f)

def trigger_retraining():
    print("Drift detected. Starting retraining...")
    try:
        subprocess.run(["python", TRAIN_SCRIPT_PATH], check=True)
        print("✅ Retraining completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during training: {e}")

def main():
    state = load_drift_state()
    if not state:
        return

    if state.get("drift_detected") is True:
        trigger_retraining()
    else:
        print("No drift detected. Skipping retraining.")

if __name__ == "__main__":
    main()
