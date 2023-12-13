import json

import pika

from app.models.task import TaskStatuses
from app.settings import settings


def send_notification(task):
    connection = pika.BlockingConnection(pika.URLParameters(settings.amqp_url))
    channel = connection.channel()

    channel.exchange_declare(exchange='orlov_notification_exchange', exchange_type='direct', durable=True)
    message_body = json.dumps(task)
    channel.basic_publish(exchange='orlov_notification_exchange', routing_key=task["user_id"],
                          body=message_body.encode('utf-8'))

    connection.close()
