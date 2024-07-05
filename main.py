from __future__ import annotations

import asyncio
import socket


async def echo(
    connection: socket,
    loop: asyncio.AbstractEventLoop,
) -> None:
    # Wait for data to be recieved on socket
    while data := await loop.sock_recv(connection, 1024):
        # Echo data back to client
        await loop.sock_sendall(connection, data)


async def listen_for_connection(
    server_socket: socket,
    loop: asyncio.AbstractEventLoop,
) -> None:
    while True:
        # Wait for new client connections
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Recieved connection from {address}')

        # Spawn off new task for handling connection with client
        asyncio.create_task(echo(connection=connection, loop=loop))


async def main():

    # Create a TCP socket for server to listen on
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set server address to localhost:8000
    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)

    # Stops blocking on socket to allow for muliple clients
    server_socket.setblocking(False)
    server_socket.listen()

    await listen_for_connection(
        server_socket=server_socket,
        loop=asyncio.get_event_loop(),
    )

asyncio.run(
    main(),
)
