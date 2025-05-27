import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime, timezone

# MQTT Broker Details
MQTT_BROKER_HOST = "localhost" # mqtt broker runs on the raspberry itself
MQTT_BROKER_PORT = 1883

# Topics to simulate data for
SENSOR_TOPICS = [
    "rover/simulated/servo/steer",

    "rover/simulated/servo/camera_x",
    "rover/simulated/servo/camera_y",

    "rover/simulated/motor/left",
    "rover/simulated/motor/right",

    "rover/simulated/led/red",
    "rover/simulated/led/blue",
    "rover/simulated/led/green",

    "rover/simulated/buzzer",

    "rover/simulated/is_online"
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

    # the actual values could be adjusted to be more realistic
    if "/motor/" in topic:
        return random.uniform(-2000, 2000) # Motor PWM values
    elif "/servo/" in topic:
        return random.uniform(-90, 90) # Servo angle
    elif "/led/" in topic:
        if random.random() < 0.5:
            return 1.0
        return 0.0
    elif "buzzer" in topic:
        if random.random() < 0.2:
            return 65535.0
        return 0.0
    elif "is_online" in topic:
        return 1.0 # value does not actually matter
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

        time.sleep(5) # Publish data for each sensor approximately every 5 seconds

except KeyboardInterrupt:
    print("Simulation stopped by user.")
except Exception as e:
    print(f"An error occurred during simulation: {e}")

finally:
    client.loop_stop() # Stop the network loop
    client.disconnect()
    print("MQTT client disconnected.")
    