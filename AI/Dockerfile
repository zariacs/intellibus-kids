# Use the official Python image (slim version to keep it lightweight)
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the required files into the container
COPY . /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to start FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
