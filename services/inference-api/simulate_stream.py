import time
import random
import requests

# Replace with your actual ELB endpoint (no trailing slash)
INFERENCE_URL = "http://a85ee0c1bdb7f4cb496137a7495d1910-715635723.us-east-2.elb.amazonaws.com:8000/predict"

# Simulate streaming input
def generate_random_features(n_features=30):
    return [round(random.uniform(-5, 5), 2) for _ in range(n_features)]

def stream_data():
    while True:
        payload = {"features": generate_random_features()}
        try:
            response = requests.post(INFERENCE_URL, json=payload)
            if response.status_code == 200:
                print("Prediction:", response.json())
            else:
                print("Error:", response.status_code, response.text)
        except Exception as e:
            print("Request failed:", e)
        
        # Wait before next simulated message
        time.sleep(2)

if __name__ == "__main__":
    print("🚀 Starting simulated streaming...")
    stream_data()

