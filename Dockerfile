FROM python:3.10-slim

# Install full LibreOffice with all export filters & Java runtime
RUN apt-get update && \
    apt-get install -y \
        libreoffice \
        libreoffice-writer \
        libreoffice-core \
        libreoffice-common \
        libreoffice-java-common \
        default-jre \
        fonts-dejavu \
        fonts-liberation \
        fonts-noto-core \
        locales \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Set LibreOffice to headless mode
ENV HOME=/tmp

# Create working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for Flask
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
