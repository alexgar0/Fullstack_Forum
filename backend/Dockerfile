FROM python:3.13-slim

# базовые настройки Python и pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

# системные зависимости (минимальный набор + без лишних рекомендаций)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# сначала зависимости — для нормального кеширования слоёв
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# потом уже весь проект
COPY . .

# не запускать всё от root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# команда запуска
CMD ["python", "-m", "src.main"]