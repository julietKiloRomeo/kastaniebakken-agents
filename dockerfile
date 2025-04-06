# Use a Python base image
FROM python:3.12

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install ChromeDriver (this version might need to match your Chrome version)
RUN apt-get update && apt-get install -y chromedriver

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY rxconfig.py .
COPY pyproject.toml .
COPY .env .
COPY morning_routine .

RUN pip install uv
RUN uv sync

# Expose the port the app will run on (assuming 3000)
EXPOSE 3000

# Run the Reflex app binding to all interfaces
CMD ["uv", "run", "reflex", "run"]
