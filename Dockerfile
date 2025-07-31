# Use official Python 3.10 slim image as base
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files to the working directory
COPY . .

ENV PYTHONPATH=/app

# Install Python dependencies (assuming requirements.txt exists)
RUN pip install --no-cache-dir -r requirements.txt

# Create .env file with HOME_DIR
ARG HOME_DIR=/app
RUN echo "HOME_DIR=${HOME_DIR}" > .env

# Command to run the application (replace main.py with actual entry point)
CMD ["python", "src/garage_payments/main.py"]