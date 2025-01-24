import asyncio

class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'connection from {peername}')
        self.transport = transport

    def data_received(self, data):    
        message = data.decode()
        print(f'Data received: {message}')

        print(f'Send: {message})')
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()
