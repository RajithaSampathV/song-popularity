# Use a slim Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend code into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Cloud Run expects
EXPOSE 8080

# Start FastAPI with uvicorn (use port 8080, not 8000)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
