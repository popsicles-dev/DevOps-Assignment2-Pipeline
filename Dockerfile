# Use a Python slim image for a smaller footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /usr/src/app

# Create the working directory
WORKDIR $APP_HOME

# Install only essential system dependencies (primarily for Pillow, Tesseract)
# Since you are using PyMySQL/mysql-connector-python, we skip libmysqlclient-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    tesseract-ocr \
    libtesseract-dev \
    libjpeg-dev \
    zlib1g-dev \
    # Add libgirepository1.0-dev if using pandas or other complex data libraries later
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to optimize Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the image
COPY . $APP_HOME

# Expose the port where Gunicorn will listen
EXPOSE 8000

# Define the default command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]