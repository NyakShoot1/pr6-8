import json

import pika

from app.models.task import TaskStatuses
from app.settings import settings


def send_notification(task):
    connection = pika.BlockingConnection(pika.URLParameters(settings.amqp_url))
    channel = connection.channel()

    if task.status == TaskStatuses.ACTIVATE:
        message = f"New task created: {task.title}"
    else:
        message = f"Task done: {task.title}"

    new_notification = {
        "message": message,
        "user_id": str(task.user_id),
        "status": str(task.status)
    }

    channel.exchange_declare(exchange='orlov_notification_created_exchange', exchange_type='direct', durable=True)
    message_body = json.dumps(new_notification)
    # channel.basic_publish(exchange='orlov_notification_created_exchange', routing_key=str(task.user_id),
    #                       body=message_body.encode('utf-8'))
    channel.basic_publish(exchange='orlov_notification_created_exchange', routing_key="notification_service",
                          body=message_body.encode('utf-8'))

    connection.close()
