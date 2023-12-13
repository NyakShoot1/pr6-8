import json
import traceback
from uuid import UUID
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings
from app.services.user_service import UserService


async def process_created_user(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        UserService().create_user(data['name'], data['email'])
        await msg.ack()
    except:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    user_created_queue = await channel.declare_queue('orlov_user_created_queue', durable=True)

    await user_created_queue.consume(process_created_user)
    print('Started RabbitMQ consuming...')

    return connection
