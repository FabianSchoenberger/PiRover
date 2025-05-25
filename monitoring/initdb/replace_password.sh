#!/bin/bash

# replaces the placeholder password in the SQL file with the actual password from the environment variable "POSTGRES_GRAFANA_PASSWORD"
SQL_FILE="01-setup-grafanadb.sql"

# Check if the POSTGRES_GRAFANA_PASSWORD environment variable is set.
if [ -z "$POSTGRES_GRAFANA_PASSWORD" ]; then
  echo "Error: POSTGRES_GRAFANA_PASSWORD environment variable is not set."
  echo "Set it before running this script."
  exit 1
fi

echo "Replacing 'grafana_password' in $SQL_FILE with the value from POSTGRES_GRAFANA_PASSWORD..."

# Use sed to replace the placeholder password with the actual password from the environment variable.
sed -i "s#grafana_password_placeholder#$POSTGRES_GRAFANA_PASSWORD#g" "$SQL_FILE"

echo "Replacement complete. Please review $SQL_FILE to ensure the change was successful."
