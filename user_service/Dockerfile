FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY user_service/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code and shared code
COPY user_service/ ./user_service
COPY common/ ./common

# Set working directory to user_service
WORKDIR /app/user_service

# Set PYTHONPATH so Python can import from /app
ENV PYTHONPATH=/app

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
