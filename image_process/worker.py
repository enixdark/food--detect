from celery import Celery
from predict import predict
import os 
import pika
import sys 
import json

app = Celery(os.getenv('BROKER_NAME') or 'tasks', 
      broker=os.getenv('BROKER_URI') or 'pyamqp://guest:guest@0.0.0.0:5672//')

app.conf.update(CELERY_ACCEPT_CONTENT = ['json','application/text'])
app.conf.update(CELERY_TASK_SERIALIZER = 'json')
# app.conf.update(CELERY_ACCEPT_CONTENT = 'json')

@app.task
def process_image(file_path,client_id):
    params = pika.URLParameters(os.getenv('RABBITMQ_URI') or 'amqp://guest:guest@0.0.0.0:5672/')
    params.socket_timeout = 5 
    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.exchange_declare(exchange='logs', type='fanout')
    data = predict(file_path)
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=str(dict(data,**{'id': client_id})))
    print(" [x] Sent %r" % str(dict(data,**{'id': client_id})))
    # connection.close()
    return file_path