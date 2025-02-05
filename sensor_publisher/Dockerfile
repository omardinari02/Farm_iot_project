FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install paho-mqtt

CMD ["python", "sensor_publisher.py"]
