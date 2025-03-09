# Use a minimal Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY consumer.py /app/consumer.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the metrics endpoint port
EXPOSE 9422

# Run the consumer
CMD ["python", "/app/consumer.py"]