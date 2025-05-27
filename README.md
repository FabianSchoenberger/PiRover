# PiRover

**PiRover** is a Wi-Fi-controlled smart vehicle based on the [Freenove Three-Wheeled Smart Car Kit for Raspberry Pi](https://www.freenove.com/). We use the hardware from the kit but implement our own custom software.

## Features

- Control via a web UI built with **Svelte** and **TailwindCSS**
- Real-time communication using **MQTT** and **WebSockets**
- Live camera streaming to the browser
- Control of LEDs, buzzer, and motors via **Python scripts** on a **Raspberry Pi 4**

## Structure

```text
/
├── monitoring/  # Data storage and visualization
├── proposal/    # Project Proposal
├── report/      # Project Report
├── rover/       # Python scripts for the Rover
├── web/         # Svelte Web Interface
```

## Running

// TODO

### Grafana and PostgreSQL (Optional)
If you just want to test the Grafana interface with simulated data:
Use the `simulated_data_dashboard.json` file in `/monitoring/grafana_dashboard_templates` instead of `data_dashboard.json` to visualize simulated data.
To insert simulated data into the PostgreSQL database, run the script `/monitoring/data_simulation/sensor_simulator.py` after step (4).
The data is similar to the data from the Rover, but not exactly the same.


To start up Grafana and PostgreSQL, which are used for data visualization the following steps are required:

1. Set the following environment variables: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_GRAFANA_PASSWORD`
2. Run the script `/monitoring/initdb/replace_password.sh` to replace the password in the `01-setup-grafanadb.sql` file. This can also be done manually.
3. In `/monitoring` run `docker compose up` to start PostreSQL and Grafana.
4. Run `python /monitoring/mqtt_to_postgres.py`, which is responsible for writing the data from the MQTT broker to the database.
5. Open Grafana in your browser at `http://localhost:3000` and log in with 'admin', 'admin'.
6. Change the credentials for Grafana if you want to.
7. Add PostreSQL as datasource in Grafana: In the `Home` page click `Add your first data source`. Choose PostgreSQL and fill in the required fields:
   - Host: value from `POSTGRES_HOST` (example: postgres:5432)
   - Database: `grafana_db`
   - User: `grafana_user`
   - Password: value from `POSTGRES_GRAFANA_PASSWORD`
   - TLS/SSL Mode: `disable`
8. Click `Save & Test` to verify the connection.
9. Import a dashboard by clicking on the `+` icon in the top right corner, then `Import dashboard`. Use the dashboard JSON file provided: `/monitoring/grafana_dashboard_templates/data_dashboard.json`.
10. Select the PostgreSQL datasource you just created and click `Import`. Now you should see the dashboard.
