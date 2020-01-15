import asyncio
import json
import websockets
import time

async def connect(websocket, path):
    print("a new user has connected!")
    async for message in websocket:
        print(message)
        if message == "prod":
            message = await producer()
            await websocket.send(message)

async def producer():
    for i in range(10):
        yield(str(i))
        time.sleep(1)

asyncio.get_event_loop().run_until_complete(
        websockets.serve(connect, 'localhost', 8765))

asyncio.get_event_loop().run_forever()
