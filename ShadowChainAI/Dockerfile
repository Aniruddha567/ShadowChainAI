# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn gradio pydantic

# Expose ports
EXPOSE 7860
EXPOSE 7861

# Run app
CMD ["python", "app.py"]