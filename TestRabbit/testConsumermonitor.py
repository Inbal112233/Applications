import pika
import os
import threading
import logging
from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "my-rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD", "2VU5D1rt31")  # Use a secret in production
QUEUE_NAME = os.getenv("QUEUE_NAME", "test_queue")

# Prometheus metric
MESSAGE_COUNT = Counter("consumer_messages_count", "Number of messages consumed")

# Connect to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

logging.info(f"Connected to RabbitMQ at {RABBITMQ_HOST}, consuming from {QUEUE_NAME}")

# Flask app for metrics
app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Start Flask in a separate thread
def start_metrics_server():
    app.run(host="0.0.0.0", port=9422)

threading.Thread(target=start_metrics_server, daemon=True).start()



# Declare the queue (must match producer settings)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

print(f" Waiting for messages from {QUEUE_NAME}. Press CTRL+C to stop.")

# Callback function to process messages
def callback(ch, method, properties, body):
    logging.info(f"Received: {body.decode()}")
    print(f" Received: {body.decode()}")
    MESSAGE_COUNT.inc()  # Increment Prometheus metric
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

# Start consuming messages
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
logging.info("Waiting for messages...")
channel.start_consuming()