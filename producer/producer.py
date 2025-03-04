import pika, logging, sys, argparse, os
from argparse import RawTextHelpFormatter
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

  #  examples = sys.argv[0] + " -p 5672 -s rabbitmq -m 'Hello' "
    #parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
     #                            description='Run producer.py',
      #                           epilog=examples)
   # parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.')
  #  parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.')
 #   parser.add_argument('-m', '--message', action='store', dest='message', help='The message to send', required=False, default='Hello')
#    parser.add_argument('-r', '--repeat', action='store', dest='repeat', help='Number of times to repeat the message', required=False, default='30')

 #   args = parser.parse_args()
  #  if args.port == None:
   #     print "Missing required argument: -p/--port"
    #    sys.exit(1)
    #if args.server == None:
     #   print "Missing required argument: -s/--server"
      #  sys.exit(1)
    print ("Producer started 2")
    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(
        rabbitmq_host, rabbitmq_port, "/", credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    #credentials = pika.PlainCredentials('guest', 'guest')
    #parameters = pika.ConnectionParameters(args.server,
     #                                      int(args.port),
      #                                     '/',
       #                                    credentials)
    #connection = pika.BlockingConnection(parameters)
    #channel = connection.channel()
    #q = channel.queue_declare('pc')
    #q_name = q.method.queue

    # Turn on delivery confirmations
    channel.confirm_delivery()

    for i in range(0, int(args.repeat)):
        if channel.basic_publish('', queue_name, "hello"):
            LOG.info('Message has been delivered')
        else:
            LOG.warning('Message NOT delivered')

        sleep(2)
    print("Producer finished repeat as requested ")
    connection.close()
    print("Producer finished1")
