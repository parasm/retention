# from celery import Celery

# QUEUE_NAME = 'flashcards'
# QUEUE_URL = 'amqp://pobtgivl:FjPvfZ7MmikOKAoumqOf9ZDjWW9omOBm@lemur.cloudamqp.com/pobtgivl'

# app = Celery('queue', broker=QUEUE_URL, BROKER_POOL_LIMIT=1)

# @app.task
# def add(x, y):
#     return x + y

import pika, os, urlparse


# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', QUEUE_URL)
url = urlparse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue=QUEUE_NAME) # Declare a queue

# send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body="message here")
print " [x] Sent 'Hello World!'"

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print " [x] Received %r" % (body)

# set up subscription on the queue
channel.basic_consume(callback,
    queue=QUEUE_NAME,
    no_ack=True)

channel.start_consuming() # start consuming (blocks)

connection.close()