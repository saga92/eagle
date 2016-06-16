#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import uuid
import imp
import os
import time

class MessageQueue(object):

    def __init__(self):
        app_conf = imp.load_source('app_conf', os.getenv('EAGLE_HOME', '..') + '/eagle_cfg.py')
        cred = pika.credentials.PlainCredentials(app_conf.MQ_USERNAME, app_conf.MQ_PASSWORD)
        parameter = pika.ConnectionParameters(host=app_conf.MQ_HOST, port=app_conf.MQ_PORT, credentials=cred)
        self.connection = pika.BlockingConnection(parameters=parameter)
        self.channel = self.connection.channel()

class UiQueue(MessageQueue):

    def __init__(self, timeout=60):
        super(UiQueue, self).__init__()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, queue=self.callback_queue,  no_ack=True)
        self.timeout = timeout

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def send(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                routing_key = 'eagle',
                properties = pika.BasicProperties(\
                    reply_to = self.callback_queue,
                    correlation_id =self.corr_id,),
                body=message
            )
        for i in xrange(self.timeout):
            if self.response is None:
                self.connection.process_data_events()
            else:
                break
            time.sleep(1)
        return self.response

class WorkerQueue(MessageQueue):

    def __init__(self):
        super(WorkerQueue, self).__init__()
        self.channel.queue_declare(queue='eagle')

    def run(self, message):
        """
        must return response
        """
        pass

    def on_request(self, ch, method, props, body):
        response = self.run(body)
        ch.basic_publish(exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id = \
                        props.correlation_id),
                body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue='eagle')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt as e:
            self.stop_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

if __name__ == '__main__':
    pass
