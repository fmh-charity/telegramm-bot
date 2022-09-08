# Отдельный сборочный образ, чтобы уменьшить финальный размер образа
FROM python:3.9-slim-bullseye as compile-image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y gcc \
 && apt-get install -y libpq-dev \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install psycopg2 \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# Окончательный образ
FROM python:3.9-slim-bullseye
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY logging.ini /app/logging.ini
COPY yoyo.ini /app/yoyo.ini
COPY bot /app/bot
RUN mkdir -p /app/logs
CMD ["python", "-m", "bot"]
#CMD ["python", "-m", "main"]