# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system deps required by PyMuPDF (mupdf) and pdf2docx if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmupdf-dev \
    libmagic1 \
  && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port and run
ENV PORT 5000
EXPOSE 5000
CMD ["python", "app.py"]
