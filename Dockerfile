FROM python:3.9.23-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей для psycopg2 и прочего
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Установка зависимостей
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]