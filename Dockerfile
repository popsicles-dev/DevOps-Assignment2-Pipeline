# Use a Python slim image for a smaller footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /usr/src/app
ENV CHROME_DRIVER_VERSION 125.0.6422.60 # Standard version for stability

# Create the working directory
WORKDIR $APP_HOME

# Install all necessary system dependencies, including Chrome/Chromedriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Existing App Dependencies
    gcc \
    tesseract-ocr \
    libtesseract-dev \
    libjpeg-dev \
    zlib1g-dev \
    # --- NEW: System dependencies required by Chrome ---
    wget \
    unzip \
    libappindicator3-1 libxss1 libasound2 \
    libnss3 libgconf-2-4 libfontconfig1 \
    # Install Google Chrome stable
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # Install ChromeDriver
    && wget -N "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip" -P /tmp/ \
    && unzip /tmp/chromedriver-linux64.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    # --- Cleanup ---
    && rm -rf /var/lib/apt/lists/* /tmp/*

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
