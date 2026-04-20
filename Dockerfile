# Use an official Python image
FROM python:3.11-slim

# Set the working folder inside the container
WORKDIR /app

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Default command
CMD ["python", "-m", "backend.orchestration.pipeline_flow"]