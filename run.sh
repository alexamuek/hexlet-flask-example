#!/bin/bash

set -e

service postgresql start

until su postgres -c "pg_isready"; do
  echo "Waiting for postgres..."
  sleep 2
done

PGPASSWORD=${PASSWORD} psql -U ${USER} -d ${DBNAME} -a -f /docker-entrypoint-initdb.d/init.sql

make prod