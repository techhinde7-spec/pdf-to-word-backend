FROM python:3.10-slim

# Install LibreOffice + required tools
RUN apt-get update && apt-get install -y libreoffice libreoffice-writer libreoffice-core && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py /app/

EXPOSE 5000

CMD ["python", "app.py"]
