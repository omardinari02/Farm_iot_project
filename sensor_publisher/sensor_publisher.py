import paho.mqtt.client as mqtt
import json
import time
import random

MQTT_BROKER = "mosquitto"  # Use the service name from Docker Compose
MQTT_PORT = 1883
MQTT_TOPIC = "farming/sensors"

def on_connect(client, userdata, flags, reason_code, properties):  # ✅ Corrected function signature
    if reason_code == 0:
        print("✅ Connected to MQTT Broker!")
    else:
        print(f"⚠️ Failed to connect, reason code {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # ✅ Use API v2 to avoid warnings
client.on_connect = on_connect

# Retry connection
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception as e:
        print(f"🚨 Connection failed: {e}, retrying in 5 seconds...")
        time.sleep(5)

client.loop_start()

while True:
    sensor_data = {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "soil_moisture": round(random.uniform(300, 700), 2),
    }
    
    client.publish(MQTT_TOPIC, json.dumps(sensor_data))
    print(f"📡 Published: {sensor_data}")
    time.sleep(5)
