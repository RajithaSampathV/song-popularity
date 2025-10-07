# Use a slim Python image
FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run expects app to listen on $PORT
ENV PORT=8080

# Expose the same port
EXPOSE 8080

# Start FastAPI using uvicorn on the correct port
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}
