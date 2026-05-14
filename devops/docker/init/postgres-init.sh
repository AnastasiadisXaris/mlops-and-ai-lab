#!/bin/bash
# Create multiple databases on first startup

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE mlflow;
    GRANT ALL PRIVILEGES ON DATABASE mlflow TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE mlops TO $POSTGRES_USER;
EOSQL

echo "Databases created: mlops, mlflow"
