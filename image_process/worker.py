from celery import Celery
from predict import predict
import os 
import pika
import sys 
app = Celery(os.getenv('BROKER_NAME') or 'tasks', 
      broker=os.getenv('BROKER_URI') or 'pyamqp://guest:guest@0.0.0.0:5672//')

@app.task
def process_image(file_path):
    params = pika.URLParameters(os.getenv('RABBITMQ_URI') or 'amqp://guest:guest@0.0.0.0:5672/')
    params.socket_timeout = 5 
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    channel.exchange_declare(exchange='logs', type='fanout')
    data = predict(file_path)
    message = ' '.join(data) or "info: Hello World!"
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=data)
    print(" [x] Sent %r" % file_path)
    # connection.close()
    return file_path