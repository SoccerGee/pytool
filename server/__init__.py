import asyncio
import sys
import functools
from pathlib import Path
import signal

async def char_generator(filename):
    dir = Path(__file__).parent
    with open(dir / filename, 'r') as file:
        for line in file:
            for char in line:
                yield char
                await asyncio.sleep(.001)

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
        args = sys.argv[1:]
        async for char in char_generator(args[0]):
            transport.write(char.encode())
    except asyncio.CancelledError:
        print("Exiting...")
    finally:
        transport.close()

asyncio.run(main())

