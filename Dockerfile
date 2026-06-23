FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-server.txt ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-server.txt

COPY . .

RUN useradd -m -u 1000 searx && chown -R searx:searx /app
USER searx

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8888/')" || exit 1

CMD ["python", "-m", "searx.webapp"]

