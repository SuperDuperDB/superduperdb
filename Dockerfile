FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    git \
    libmagic1 \
    libpq-dev \
    unixodbc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy repository code
COPY . .

# Install package with test dependencies
RUN pip install --no-cache-dir -e ".[test]"

# Fix loki_logger_handler import issue
RUN sed -i 's/from loki_logger_handler.loki_logger_handler import LoguruFormatter, LokiLoggerHandler/from loki_logger_handler.loki_logger_handler import LoggerFormatter as LoguruFormatter, LokiLoggerHandler/' /app/superduper/base/logger.py

CMD ["python"]