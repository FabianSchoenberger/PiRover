-- TODO: use env variables

CREATE USER "grafana_user" WITH PASSWORD 'grafana_password';
CREATE DATABASE grafana_db;

\connect grafana_db

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- One table for all rover readings, sensors will be differentiated by the sensor_topic column
CREATE TABLE IF NOT EXISTS rover_readings (
    id SERIAL NOT NULL,
    time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
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
