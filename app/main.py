from fastapi import FastAPI, WebSocket
from app.websocket_manager import manager
import asyncio
from app.epbx_listener import start_listener

app = FastAPI()


@app.on_event("startup")
async def startup():

    asyncio.create_task(start_listener())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except:
        manager.disconnect(websocket)