FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    bluez \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY run.py .

RUN pip install pyhatchbabyrest bleak paho-mqtt

CMD ["python3", "run.py"]
