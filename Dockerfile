FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_NO_CACHE_DIR=1 \
	DATABASE_DIR=/app/database \
	DB_FILE=/app/database/tradingplatform.db \
	LOG_FILE=/app/logs/tradingplatform.log

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

COPY src/ .

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
	&& mkdir -p /app/database /app/logs \
	&& chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
