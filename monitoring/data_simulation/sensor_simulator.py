import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime, timezone

# MQTT Broker Details
MQTT_BROKER_HOST = "localhost" # Or the IP/hostname of your MQTT broker
MQTT_BROKER_PORT = 1883

# Topics to simulate data for
SENSOR_TOPICS = [
    "rover/motor/left/pwm",
    "rover/motor/right/pwm",
    "rover/servo/steer_angle",
    "rover/servo/camera_x",
    "rover/servo/camera_y",
    "rover/temperature",
]

# --- MQTT Client Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

client.on_connect = on_connect

try:
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    client.loop_start()
except ConnectionRefusedError:
    print(f"Connection refused. Make sure your MQTT broker is running at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
    exit()
except Exception as e:
    print(f"An error occurred connecting to MQTT: {e}")
    exit()


# --- Data Simulation Loop ---

def simulate_sensor_value(topic):
    """Generates a simulated value based on the topic."""
    if "pwm" in topic:
        return random.uniform(0, 255) # Motor PWM values
    elif "steer_angle" in topic:
        return random.uniform(-90, 90) # Servo angle
    elif "camera_" in topic:
        return random.uniform(-50, 50) # Camera position (example range)
    elif "temperature" in topic:
        return random.uniform(20, 30) # Temperature in Celsius
    else:
        return random.random() # Default random value

print("Starting data simulation...")
try:
    while True:
        for topic in SENSOR_TOPICS:
            value = simulate_sensor_value(topic)
            timestamp = datetime.now(timezone.utc).isoformat()
            payload = json.dumps({
                "value": round(value, 5),
                "timestamp": timestamp
            })

            client.publish(topic, payload)
            print(f"Published to {topic}: {payload}")

        time.sleep(1) # Publish data for each sensor approximately every 1 second

except KeyboardInterrupt:
    print("Simulation stopped by user.")
except Exception as e:
    print(f"An error occurred during simulation: {e}")

finally:
    client.loop_stop() # Stop the network loop
    client.disconnect()
    print("MQTT client disconnected.")
    