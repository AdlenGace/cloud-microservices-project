# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy Python requirements first (for faster caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all service code
COPY . .

# Expose the port (adjust per service)
EXPOSE 8000

# Command to run the service
CMD ["python", "app.py"]
