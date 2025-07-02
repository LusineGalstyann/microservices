
FROM python:3.11-slim


# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY post_service/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy only post_service and shared common folder
COPY post_service/ ./post_service
COPY common/ ./common

# Set working directory to the app code
WORKDIR /app/post_service

# Set PYTHONPATH so modules like `common` can be imported
ENV PYTHONPATH=/app

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
