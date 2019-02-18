#!/usr/bin/env python3

"""
NOTEPADAI
(Main script)

Server to transcript audio streams and send them back
"""

import socket

HOST = '127.0.0.1'  # Server name
PORT = 12345         # Standard RTP port
CHUNK = 1024

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen(5)

while True:
    connection, address = socket.accept()
    data = connection.recv(CHUNK)

    print(data)