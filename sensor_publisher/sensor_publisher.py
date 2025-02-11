import paho.mqtt.client as mqtt
import random
import time
import configparser
import threading

# Load MQTT configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

MQTT_BROKER = "mosquitto"  # Use the service name from Docker Compose
MQTT_PORT = 1883

farms = int(config['data_generation']['farms'])  # Number of farms
time_sleep = int(config['data_generation']['time_sleep'])  # Delay between publishing
sensors = config['data_generation']['sensors'].split('|')  # Sensor types

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, port=MQTT_PORT)

# Function to publish farm data to MQTT broker
def publish_farm_data(mqtt_client, sensors, farm):
    while True:
        # Generate random sensor data for each sensor type
        for sensor in sensors:
            if sensor == 'temperature':
                data = round(random.uniform(0, 50), 2)  # Simulating temperature
            elif sensor == 'humidity':
                data = round(random.uniform(30, 90), 2)  # Simulating humidity
            elif sensor == 'soil_moisture':
                data = random.randint(200, 700)  # Simulating soil moisture
            elif sensor == 'light_intensity':
                data = random.randint(0, 1100)  # Simulating light intensity

            # Construct structured MQTT topic
            topic = f"farming/farm_{farm}/{sensor}"
            
            # Publish data in JSON format
            payload = f'{{"{sensor}": {data}, "farm": "farm_{farm}"}}'
            mqtt_client.publish(topic, payload)
            print(f"Published {topic}: {payload}")

        time.sleep(time_sleep)  # Delay between publishing data

# Start publishing data using multiple threads (one per farm)
threads = []
for farm in range(1, farms + 1):  # Starts from farm_1
    thread = threading.Thread(target=publish_farm_data, args=(mqtt_client, sensors, farm))
    threads.append(thread)
    thread.start()

# Keep threads running
for thread in threads:
    thread.join()
