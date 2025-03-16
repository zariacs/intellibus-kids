# Use a smaller Alpine-based image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install Alpine dependencies (important for some Python libraries)
RUN apk add --no-cache gcc musl-dev libffi-dev

# Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Copy and install dependencies first (for Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI app
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
