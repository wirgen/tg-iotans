FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -U pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml  ./
RUN pip install --no-cache-dir .

COPY . ./

ENTRYPOINT ["python", "-m", "tg_iotans"]