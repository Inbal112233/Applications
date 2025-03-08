import pika, logging, sys, os
from time import sleep

if __name__ == '__main__':
    print ("Producer started 1")

    # Retrieve environment variables
    rabbitmq_host = os.environ.get("RABBITMQ_HOST")
    rabbitmq_port = int(os.environ.get("RABBITMQ_PORT", 5672))  # Default to 5672
    rabbitmq_user = os.environ.get("RABBITMQ_USER")
    rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")
    queue_name = os.environ.get("QUEUE_NAME")

    # Print the retrieved variables
    print(f"RabbitMQ Host: {rabbitmq_host}")
    print(f"RabbitMQ Port: {rabbitmq_port}")
    print(f"RabbitMQ User: {rabbitmq_user}")
    print(f"RabbitMQ Password: {rabbitmq_password}")
    print(f"Queue Name: {queue_name}")


    print ("sleep 5")
    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, "/", credentials)

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        # Turn on delivery confirmations
        channel.confirm_delivery()

        for i in range(0, 30):  # Default repeat count
            if channel.basic_publish('', queue_name, "hello"):
                LOG.info('Message has been delivered')
            else:
                LOG.warning('Message NOT delivered')

            sleep(2)

        print("Producer finished repeat as requested")
    except pika.exceptions.AMQPConnectionError as e:
        LOG.error(f"Error connecting to RabbitMQ: {e}")
    finally:
        connection.close()
        print("Producer finished1")