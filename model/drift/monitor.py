import numpy as np
import json
import os
import requests

DRIFT_STATE_FILE = os.path.join(os.path.dirname(__file__), "drift_state.json")
DRIFT_THRESHOLD = 0.1  # Adjust threshold as needed


def load_reference_data(path="reference_data.npy"):
    return np.load(path)


def load_live_data(path="live_batch.npy"):
    return np.load(path)


def detect_drift(ref_data, live_data):
    # Compare mean and std dev shift
    mean_diff = np.abs(np.mean(ref_data) - np.mean(live_data))
    std_diff = np.abs(np.std(ref_data) - np.std(live_data))
    mean_threshold = DRIFT_THRESHOLD * np.std(ref_data)
    std_threshold = DRIFT_THRESHOLD * np.std(ref_data)

    drifted = mean_diff > mean_threshold or std_diff > std_threshold

    return {
        "mean_diff": float(mean_diff),
        "std_diff": float(std_diff),
        "drift_detected": bool(drifted)
    }


def write_drift_state(result):
    with open(DRIFT_STATE_FILE, "w") as f:
        json.dump(result, f, indent=2)


def trigger_github_workflow():
    token = os.environ.get("GH_PAT")
    if not token:
        print("No GH_PAT found. Skipping GitHub workflow trigger.")
        return

    repo = "gouthamyadavganta/mlops-anomaly-detection"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/train-model.yml/dispatches"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "ref": "main"  # Change to your branch name if not 'main'
    }

    response = requests.post(url, headers=headers, json=data)
    print("Triggered GitHub workflow:", response.status_code, response.text)


def main():
    ref = load_reference_data()
    live = load_live_data()
    result = detect_drift(ref, live)
    write_drift_state(result)
    print(json.dumps(result, indent=2))

    if result.get("drift_detected"):
        trigger_github_workflow()


if __name__ == "__main__":
    main()

