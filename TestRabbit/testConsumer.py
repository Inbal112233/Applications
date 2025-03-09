import pika
import os

# Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "my-rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD", "2VU5D1rt31")  # Use a secret in production
QUEUE_NAME = "test_queue"

# Connect to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue (must match producer settings)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

print(f"🐇 Waiting for messages from {QUEUE_NAME}. Press CTRL+C to stop.")

# Callback function to process messages
def callback(ch, method, properties, body):
    print(f"✅ Received: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

# Start consuming messages
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
channel.start_consuming()