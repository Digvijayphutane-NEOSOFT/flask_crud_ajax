# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

## Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy application code and any other necessary files
COPY . .

# Set environment variables (for DB connection, etc.) from config.py or other sources
# COPY config.py ./

# Expose the Flask application port
EXPOSE 5000

# Define environment variable
# ENV NAME venv

# Run app.py when the container launches
CMD ["python", "app.py"]
