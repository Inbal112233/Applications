import pika, logging
import time
import os,sys

#import threading
#import logging
#import time
from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Starting consumer")
time.sleep(30)

# Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "my-rabbitmq")  # Default service name in Minikube
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")  # Adjust if needed
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD", "2VU5D1rt31")  # Use secret in production
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
QUEUE_NAME = os.getenv("QUEUE_NAME", "pc")
X_SECONDS = int(os.getenv("MESSAGE_INTERVAL", 5))  # Every X seconds
#Y_TIMES = int(os.getenv("MESSAGE_COUNT", 10))  # removed once moved to endless loop

logging.debug(f" finished reading env variables ")

# Prometheus metric
MESSAGE_COUNT = Counter("consumer_messages_count", "Number of messages consumed")
# Connect to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue (idempotent)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

logging.debug(f"Connected to RabbitMQ at {RABBITMQ_HOST}, consuming messages to {QUEUE_NAME}")

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


counter1 = 1
while True:
    message = f"Message {counter1}"
    logging.info(f"Sent: {message}")
    counter1 += 1
    time.sleep(10)

#for debugging crashes
time.sleep(300)

'''
counter1 = 1
while True:
    message = f"Message {counter1}"
    print(f" Sent: {message}")
    logging.info(f"Sent: {message}")
    counter1 += 1
    time.sleep(10)
'''
'''
try:
    RABBITMQ_PORT = int(RABBITMQ_PORT_STR)  # Convert to integer *just before use*
except ValueError:
    print(f"Error: Invalid RABBITMQ_PORT: {RABBITMQ_PORT_STR}. Must be an integer.")
    # Handle the error appropriately (e.g., exit, use a default)
    exit(1)  # Or use a default port
'''
'''
# Flask app for metrics
app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Start Flask in a separate thread
def start_metrics_server():
    app.run(host="0.0.0.0", port=9422)

threading.Thread(target=start_metrics_server, daemon=True).start()
'''



