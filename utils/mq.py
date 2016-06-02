#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
from eagle import app

class MessageQueue:

    connection = None
    channel = None

    @classmethod
    def connect(cls):
        if cls.connection is None or cls.connection.is_closed is True:
            cred = pika.credentials.PlainCredentials(app.config['MQ_USERNAME'], app.config['MQ_PASSWORD'])
            parameter = pika.ConnectionParameters(host=app.config['MQ_HOST'], port=app.config['MQ_PORT'], credentials=cred)
            cls.connection = pika.BlockingConnection(parameters=parameter)
            cls.channel = cls.connection.channel()

    @classmethod
    def send(cls, message):
        cls.channel.queue_declare(queue='eagle', durable=True)
        cls.channel.basic_publish(exchange='amq.direct',\
            routing_key='eagle',\
            body=message, \
            properties=pika.BasicProperties(content_type='application/json', \
                delivery_mode=2)) # make message persistent

    @classmethod
    def disconnect(cls):
        cls.connection.close()

    @classmethod
    def start_consuming(cls):
        cls.channel.basic_consume(cls.on_message, 'eagle')
        try:
            cls.channel.start_consuming()
        except KeyboardInterrupt:
            cls.channel.stop_consuming()

    @classmethod
    def stop_consuming(cls):
        cls.channel.stop_consuming()

    @classmethod
    def on_message(cls, channel, method_frame, header_frame, body):
        cls.process_message(body)
        cls.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    @classmethod
    def process_message(cls, message_body):
        pass

if __name__ == '__main__':
    MessageQueue.connect()
    MessageQueue.send('lala')
    MessageQueue.disconnect()
    class Client(MessageQueue):
        @classmethod
        def process_message(cls, message_body):
            print message_body
    Client.connect()
    Client.start_consuming()
    Client.disconnect()
