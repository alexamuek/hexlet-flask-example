#!/usr/bin/env bash

# Ждём, пока БД запустится
sleep 3

# Выполняем init.sql с правильным пользователем
docker exec -i -e PGPASSWORD=mypassword my-pg psql -U myuser -d mydb < init.sql