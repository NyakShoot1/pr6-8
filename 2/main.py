import asyncio
from fastapi import FastAPI
from app import rabbitmq
from app.endpoints.user_router import user_router

app = FastAPI(title='User service')


@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(user_router, prefix='/api')
