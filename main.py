from __future__ import annotations

import selectors
import socket

# Let library select the best selector for our OS
selector = selectors.DefaultSelector()

# Create a TCP socket for server to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set server address to localhost:8000
server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)

# Stops blocking on socket to allow for muliple clients
server_socket.setblocking(False)
server_socket.listen()

# Register server socket for OS read notifications
selector.register(server_socket, selectors.EVENT_READ)

while True:
    # select returns when an event happens, returning a list of sockets
    # to be processed, or an empty list on a timeout.
    events: list[
        tuple[selectors.SelectorKey, int]
    ] = selector.select(timeout=1)

    if len(events) == 0:
        print('No Events, timeout reached')

    for event, _ in events:
        # Get socket where event occured
        event_socket = event.fileobj

        # This is a connection attempt on the server
        if event_socket == server_socket:
            connection, address = server_socket.accept()

            # Allow for mulitple connections
            connection.setblocking(False)

            # Register new client
            selector.register(connection, selectors.EVENT_READ)

            print(f'Server connected with {address}')
        else:  # Recieving data from client

            # Read in Kibibyte of data from socket
            data = event_socket.recv(1024)
            event_socket.send(data)

            print(f'Echoing {data} back to client')
