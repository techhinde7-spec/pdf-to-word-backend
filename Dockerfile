# Use Python base image
FROM python:3.11-slim

# Install system dependencies (LibreOffice + fonts + wget for debugging)
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Render requires listening on 0.0.0.0:$PORT
ENV PORT=10000

# Command to run Flask
CMD ["python", "app.py"]
