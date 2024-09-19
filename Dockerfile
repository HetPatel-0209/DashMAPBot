# Use an official Python runtime as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system packages (you can add more as needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libffi-dev \
    python3-dev

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]