import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import psycopg2
import json
import os
from datetime import datetime, timezone
import time

load_dotenv()

# --- Database Details ---
DB_HOST = "localhost"
DB_NAME = "grafana_db"
DB_USER = "grafana_user"
DB_PASSWORD = os.getenv("POSTGRES_GRAFANA_PASSWORD")

if not DB_NAME or not DB_USER or not DB_PASSWORD:
    print("Database environment variables not set. Check your configuration.")
    exit(1)

# --- MQTT Broker Details ---
MQTT_BROKER_HOST = "localhost" # mqtt broker runs on the raspberry itself
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_SUBSCRIBE = "rover/#" # Subscribe to all topics under 'rover/'

# --- Database Connection ---
conn = None
cursor = None

def connect_db():
    global conn, cursor
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        print("Database connection established.")
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        print("Retrying database connection in 5 seconds...")
        time.sleep(5)
        connect_db() # Retry connection
    except Exception as e:
        print(f"An unexpected database error occurred: {e}.")
        print("Retrying database connection in 5 seconds...")
        time.sleep(5)
        connect_db()

# --- MQTT Client Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
        print(f"Subscribed to topic: {MQTT_TOPIC_SUBSCRIBE}")
    else:
        print(f"Failed to connect to MQTT, return code {rc}\n")
        print("Retrying connection in 5 seconds...")
        time.sleep(5)
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    try:
        data = json.loads(payload)
        value = data.get("value")
        timestamp_str = data.get("timestamp")

        if value is None:
            print(f"Warning: Received payload without 'value' on topic {topic}. Skipping.")
            return

        timestamp = None
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                if timestamp.tzinfo is None:
                     timestamp = timestamp.replace(tzinfo=timezone.utc)
            except ValueError:
                print(f"Warning: Invalid timestamp format '{timestamp_str}' on topic {topic}. Using database default.")

        # Insert
        if conn and cursor:
            try:
                insert_sql = """
                INSERT INTO rover_readings (time, sensor_topic, value)
                VALUES (%s, %s, %s);
                """
                cursor.execute(insert_sql, (timestamp, topic, value))
                conn.commit()
            except Exception as db_err:
                print(f"Database insert error: {db_err}")
                conn.rollback()
                # ignore this one data point
        else:
            print("Database connection not available.")

    except json.JSONDecodeError:
        print(f"Error decoding JSON payload on topic {topic}: {payload}")
    except Exception as e:
        print(f"An unexpected error occurred processing message on topic {topic}: {e}")


client.on_connect = on_connect
client.on_message = on_message

if __name__ == "__main__":
    connect_db()

    if not conn:
        print("Failed to connect to the database. Exiting.")
        exit()

    try:
        print("Starting MQTT client loop...")
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        client.loop_forever()

    except KeyboardInterrupt:
        print("Ingestion stopped by user.")
    except ConnectionRefusedError:
        print(f"Connection refused. Make sure your MQTT broker is running at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
    except Exception as e:
        print(f"An error occurred during MQTT processing: {e}")

    finally:
        print("Cleaning up and exiting mqtt_to_postgres.py...")
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Database connection closed.")
        client.disconnect()
        print("MQTT client disconnected.")