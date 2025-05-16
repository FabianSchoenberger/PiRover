import asyncio
import threading

import websockets as ws


async def _serve(handler):
    async with ws.serve(handler, "0.0.0.0", 80) as server:
        await server.serve_forever()


def _start(handler):
    asyncio.run(_serve(handler))


def start(handler):
    thread = threading.Thread(target=_start, args=(handler,))
    thread.start()
    return thread


async def send(websocket, payload):
    await websocket.send(payload)
