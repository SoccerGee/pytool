import asyncio
import sys
import functools
import signal
import os

from pathlib import Path
from typing import Generator

from .protocols import EchoServerProtocol

'''
call using:
    async for char in char_generator('file.txt'):
        transport.write(char.encode())
'''
async def char_generator(filename: str): -> Generator[str, None, None]
    dir = Path(__file__).parent
    with open(dir / filename, 'r') as file:
        for line in file:
            for char in line:
                yield char
                await asyncio.sleep(.001)

# @TODO: declare new typing for returning a server protocol
def get_server_protocol():
    server_var = os.environ.get('SERVER','echo').lower()
    match server_var:
        case 'echo':
            print(f'FOUND {server_var} SERVER')
            server = EchoServerProtocol.EchoServer
        case _:
            print(f'NO SERVER WITH THE TYPE \'{server_var}\' FOUND')
            print('Running echo server...')
            server = EchoServerProtocol.EchoServer
    return server

'''
close all asyncio tasks
'''
def exit_signal_handler():
    for task in asyncio.all_tasks():
        task.cancel()

async def main():
    loop = asyncio.get_running_loop()

    transport, _ = await loop.connect_write_pipe(
        asyncio.Protocol,
        sys.stdout.buffer
    )

    loop.add_signal_handler(signal.SIGINT, exit_signal_handler)

    try:
        server = await loop.create_server(
                get_server_protocol(),
                '127.0.0.1', 8888)
        async with server:
            await server.serve_forever()
    except asyncio.CancelledError:
        print("Exiting...")
    finally:
        transport.close()

asyncio.run(main())

