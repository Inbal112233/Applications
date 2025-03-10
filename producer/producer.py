
import pika, logging, sys, os
import time


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Starting Producer")
print(f" Starting Producer")
#for debugging crashes
time.sleep(30)

# Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")  # Default service name in Minikube
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")  # Adjust if needed
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD", "2VU5D1rt31")  # Use secret in production
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
QUEUE_NAME = os.getenv("QUEUE_NAME", "test_queue")
X_SECONDS = int(os.getenv("MESSAGE_INTERVAL", 5))  # Every X seconds
#Y_TIMES = int(os.getenv("MESSAGE_COUNT", 10))  # removed once moved to endless loop

logging.debug(f" finished reading env variables ")
print(f" finished reading env variables")

# Connect to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue (idempotent)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

logging.debug(f"Connected to RabbitMQ at {RABBITMQ_HOST}, sending messages to {QUEUE_NAME}")
print(f" fConnected to RabbitMQ ")

for i in range(1, 5 + 1):
    message = f"Message {i} from producer"
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)
    logging.info(f"Sent: {message}")
    time.sleep(X_SECONDS)

counter = 6
while True:
    message = f"Message {counter} from producer"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    logging.info(f"Sent: {message}")
    counter += 1
    time.sleep(X_SECONDS)  # Wait 20 seconds before sending the next message
'''
counter1 = 1
while True:
    message = f"Message {counter1}"
    print(f" Sent: {message}")
    logging.info(f"Sent: {message}")
    counter1 += 1
    time.sleep(10)

logging.info(f"completed sending messages ")
time.sleep(120)
'''
