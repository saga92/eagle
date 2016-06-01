#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika

parameters = pika.URLParameters('amqp://root:root123@192.168.99.100:8082/')

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.basic_publish(exchange='amq.direct',
        routing_key='eagle',\
        body='create_time', \
        pika.BasicProperties(content_type='text/plain', \
            delivery_mode=1))

connection.close()
