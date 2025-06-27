# Use official Python image (slim version for smaller size)
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Expose port (if needed, though Cloud Run/K8s can specify)
EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
