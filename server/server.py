import socket
import select
import threading
import time
import math
import os
import sys

#Import Utilities
from utils.constants import SERVER_RECV_PORT, SERVER_CAPACITY
from utils.helpers import get_self_ip
from utils.socket_functions import recvall





def Main():
    # Get IP of the server
    server_ip = get_self_ip()
    print('Server is hosted at: ',server_ip)

    # Socket to listen for incoming connections from peers
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuring the socket to reuse addresses and immediately transmit data
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    server_socket.bind((IP, SERVER_RECV_PORT))
    server_socket.listen(SERVER_CAPACITY)

    # List of connected peers
    sockets_list = [server_socket]
    # To lookup IP of a given username
    uname_to_ip: dict[str, str] = {}
    # To lookup username of a given IP
    ip_to_uname: dict[str, str] = {}
    # Mapping from username to last seen timestamp
    uname_to_status: dict[str, float] = {}

    while True:


if __name__ == '__main__':
    Main()
