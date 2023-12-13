import asyncio
from fastapi import FastAPI
from app import rabbitmq_consume
from app.endpoints.task_router import task_router

app = FastAPI(title='Task service')


@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq_consume.consume(loop))


app.include_router(task_router, prefix='/api')
