from celery import Celery
import os 
import pika
import sys 
app = Celery(os.getenv('BROKER_NAME') or 'tasks', 
      broker=os.getenv('BROKER_URI') or 'pyamqp://guest:guest@0.0.0.0:5672//')

@app.task
def process_image(file_path):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URI') or 'amqp://guest:guest@localhost:5672'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', type='fanout')

    message = ' '.join(file_path) or "info: Hello World!"
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % file_path)
    connection.close()
    return file_path