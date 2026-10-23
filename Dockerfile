# Use an official lightweight Python image based on Linux
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (optimizes Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application source code into the container
COPY health_agent.py .

# Define the command to run when the container starts
CMD ["python", "health_agent.py"]