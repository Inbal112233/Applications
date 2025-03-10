import pika
import os
import time
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info(f"Starting Producer ")
print(f" Starting Producer")

# Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "my-rabbitmq")  # Default service name in Minikube
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")  # Adjust if needed
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD", "2VU5D1rt31")  # Use secret in production
QUEUE_NAME = os.getenv("QUEUE_NAME", "test_queue")
X_SECONDS = int(os.getenv("MESSAGE_INTERVAL", 5))  # Every X seconds
#Y_TIMES = int(os.getenv("MESSAGE_COUNT", 10))  # removed once moved to endless loop

logging.info(f" finished reading env variables ")
print(f" finished reading env variables ")
"""
# Connect to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue (idempotent)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

logging.info(f"Connected to RabbitMQ at {RABBITMQ_HOST}, sending messages to {QUEUE_NAME}")

print(f" Connected to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}, sending {Y_TIMES} messages every {X_SECONDS} seconds...")

# Send messages in a loop
#for i in range(1, Y_TIMES + 1):
#    message = f"Message {i} from producer"
#    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)
#    print(f" Sent: {message}")
#    time.sleep(X_SECONDS)
# Cleanup
#connection.close()
#print(" Finished sending messages.")

# Infinite loop to send messages every 20 seconds
counter = 1
print(" Producer started, sending messages every 20 seconds...")

while True:
    message = f"Message {counter}"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    print(f" Sent: {message}")
    logging.info(f"Sent: {message}")
    counter += 1
    time.sleep(X_SECONDS)  # Wait 20 seconds before sending the next message
"""
counter = 1
while True:
    message = f"Message {counter}"
    print(f" Sent: {message}")