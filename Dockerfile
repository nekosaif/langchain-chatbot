FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for FAISS
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p /app/app/vector_store

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]