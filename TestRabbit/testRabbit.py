import pika
import os

# RabbitMQ connection details
RABBITMQ_HOST = "my-rabbitmq.default.svc.cluster.local"  # Service name in Kubernetes
RABBITMQ_PORT = 5672
RABBITMQ_USER = "user"  # Change if using a different user
RABBITMQ_PASS = "2VU5D1rt31"

# Establish connection
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare a test queue
    channel.queue_declare(queue="test_queue")

    # Send a message
    message = "Hello, RabbitMQ! Authentication works!"
    channel.basic_publish(exchange="", routing_key="test_queue", body=message)

    print(f"[✓] Sent: {message}")

    # Close connection
    connection.close()
except Exception as e:
    print(f"[X] Connection failed: {e}")