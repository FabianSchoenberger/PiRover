CREATE USER "grafana_user" WITH PASSWORD 'grafana_password_placeholder'; -- grafana_password_placeholder
CREATE DATABASE grafana_db;

\connect grafana_db

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- One table for all rover readings, sensors will be differentiated by the sensor_topic column
CREATE TABLE IF NOT EXISTS rover_readings (
    id SERIAL NOT NULL,
    time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    sensor_topic TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (id, time)
);

-- Convert the table to a TimescaleDB hypertable
SELECT create_hypertable('rover_readings', 'time');

GRANT SELECT, INSERT, UPDATE, DELETE ON public.rover_readings TO grafana_user;

GRANT USAGE ON SCHEMA public TO grafana_user;
GRANT CREATE ON SCHEMA public TO grafana_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO grafana_user;
GRANT USAGE, SELECT ON SEQUENCE rover_readings_id_seq TO grafana_user;

CREATE INDEX ON rover_readings (sensor_topic, time DESC);

-- Rover sends a periodic state to 'rover/isOnline' as long as it is running. 
-- For each timestamp between p_start and p_end, spaced by p_step (e.g. every 15 seconds), we check whether a status update was received within the surrounding p_threshold window (e.g. within ±15 seconds of that time).
-- If the Rover is offline it does not send any data and we assume it is offline - this is why the function is rather complex.
CREATE OR REPLACE FUNCTION get_device_uptime(p_sensor_topic TEXT, p_start TIMESTAMPTZ, p_end TIMESTAMPTZ, p_step INTERVAL, p_threshold INTERVAL DEFAULT '15 seconds')
RETURNS TABLE(ts TIMESTAMPTZ, is_online INT) AS $$
WITH time_series AS (
  SELECT generate_series(p_start, p_end, p_step) AS ts
),
last_seen_up AS (
  SELECT time FROM rover_readings
  WHERE sensor_topic = p_sensor_topic
    AND time BETWEEN p_start AND p_end
)
SELECT
  t.ts,
  COALESCE((
    SELECT 1
    FROM last_seen_up u
    WHERE ABS(EXTRACT(EPOCH FROM (t.ts - u.time))) <= EXTRACT(EPOCH FROM p_threshold)
    ORDER BY u.time DESC
    LIMIT 1
  ), 0) AS is_online
FROM time_series t
ORDER BY t.ts;
$$ LANGUAGE sql STABLE;

GRANT EXECUTE ON FUNCTION get_device_uptime(TEXT, TIMESTAMPTZ, TIMESTAMPTZ, INTERVAL, INTERVAL) TO grafana_user;
