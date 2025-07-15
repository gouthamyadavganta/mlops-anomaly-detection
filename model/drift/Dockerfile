FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly copy .py and .npy files
COPY monitor.py . 
COPY auto_retrain.py .
COPY reference_data.npy .
COPY live_batch.npy .

CMD ["python", "monitor.py"]

