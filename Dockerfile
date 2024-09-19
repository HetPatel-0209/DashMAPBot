# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the Rasa project files and Flask API files into the container
COPY . /app

EXPOSE 5000

# Run Rasa and Flask API simultaneously
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=5000"]