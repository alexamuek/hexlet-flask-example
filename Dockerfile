FROM python:3.14-slim

# Переменные для создания пользователя БД (те же, что и в run.sh)
ARG USER
ARG PASSWORD
ARG DBNAME

# Дефолтные значения
ENV USER=${USER:-docker} \
    PASSWORD=${PASSWORD:-docker} \
    DBNAME=${DBNAME:-docker}

RUN apt-get update && apt-get install -yqq \
    make \
    postgresql-17 \
    sudo \
    curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

COPY init.sql /docker-entrypoint-initdb.d/

# postgres config
RUN echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/17/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/17/main/postgresql.conf

# create docker user and db (используем те же переменные, что в run.sh)
RUN service postgresql start && \
    su postgres -c "psql --command \"CREATE USER ${USER} WITH SUPERUSER PASSWORD '${PASSWORD}';\"" && \
    su postgres -c "createdb -O ${USER} ${DBNAME}" && \
    service postgresql stop

COPY run.sh ./run.sh
RUN chmod +x ./run.sh

CMD ./run.sh