FROM python:3.10-slim

# Install LibreOffice with DOCX export filters + Java (required for some filters)
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer default-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set LibreOffice in headless mode
ENV HOME=/tmp

# Copy requirements and install Python packages
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Run Flask app
CMD ["python", "app.py"]
