#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

def on_messaage(channel, method_frame, header_frame, body):
    print method_frame.delivery_tag
    print body
    print
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

connection = pika.BlockingConnection()
channel = connection.channel()
channel.basic_consume(on_message, 'test')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
