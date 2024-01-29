import socket
import select
import threading
import time
import math
import os
import sys

#Import Utilities
from utils.exceptions import ExceptionCode, RequestException
from utils.constants import APP_DIR, SERVER_CAPACITY, SERVER_RECV_PORT
from utils.helpers import get_self_ip
from utils.socket_functions import recvall
from utils.types import SocketMessage

app_dir = APP_DIR
logs_dir = app_dir / "logs"
database_dir = app_dir / "db"

app_dir.mkdir(exist_ok=True)
(logs_dir).mkdir(exist_ok=True)
(database_dir).mkdir(exist_ok=True)

def log(message: str, log_type: str = "INFO"):
    """Utility to log messages to a file.

    Parameters
    ----------
    message : str
        Message to be logged.
    log_type : str, optional
        Type of the message, by default "INFO".
    """
    log_file = logs_dir / "server.log"
    with open(log_file, "a") as file:
        file.write(f"[{log_type}] {message}\n")

def receive_request(client_socket: socket.socket) -> SocketMessage:
    """Receives incoming requests from peers

    Parameters
    ----------
    client_socket : socket.socket
        The socket on which to receive the message

    Returns
    ----------
    SocketMessage
        The type of the message and query received from the peer

    Raises
    ----------
    RequestException
        In case of any exceptions that occur in receiving the message
    """
    
    try:
        # Receive message type
        message_type = client_socket.recv(HEADER_TYPE_LEN).decode(FMT)
        if not len(message_type):
            raise RequestException(
                msg=f"Client at {client_socket.getpeername()} closed the connection",
                code=ExceptionCode.DISCONNECT,
            )
        if message_type not in [
            HeaderCode.NEW_CONNECTION.value,
            HeaderCode.REQUEST_IP.value,
            HeaderCode.REQUEST_UNAME.value,
            HeaderCode.SHARE_DATA.value,
            HeaderCode.FILE_BROWSE.value,
            HeaderCode.FILE_SEARCH.value,
            HeaderCode.UPDATE_HASH.value,
            HeaderCode.HEARTBEAT_REQUEST.value,
        ]:
            logging.error(msg=f"Received message type {message_type}")
            raise RequestException(
                msg=f"Invalid message type in header, received: {message_type}",
                code=ExceptionCode.INVALID_HEADER,
            )
        elif message_type == HeaderCode.HEARTBEAT_REQUEST.value:
            # Update online status
            return {"type": HeaderCode(message_type), "query": "online"}
        else:
            # If any query is sent, update the last seen to the current time
            username = ip_to_uname.get(notified_socket.getpeername()[0])
            if username is not None:
                uname_to_status[username] = time.time()
            elif message_type != HeaderCode.NEW_CONNECTION.value:
                raise RequestException(
                    msg=f"Username does not exist",
                    code=ExceptionCode.NOT_FOUND,
                )

            # Receive the query and return it
            message_len = int(client_socket.recv(HEADER_MSG_LEN).decode(FMT))
            logging.debug(
                msg=f"Receiving packet: TYPE {message_type} LEN {message_len} from {client_socket.getpeername()}"
            )
            query = recvall(client_socket, message_len)
            return {"type": HeaderCode(message_type), "query": query}
    except Exception as e:
        logging.exception(f"Error receiving from peer: {e}")
        return {"type": HeaderCode.ERROR, "query": "Failed to receive"}


def read_handler(notified_socket: socket.socket):
    global uname_to_ip
    global ip_to_uname
    global sockets_list

    # New connection
    if notified_socket == server_socket:
        # Accept the connection and add it to the list of connected peers
        client_socket, client_addr = server_socket.accept()
        sockets_list.append(client_socket)
        print(f"Accepted new connection from {client_addr[0]}:{client_addr[1]}")

    return 


def Main():
    global server_socket
    global uname_to_ip
    global ip_to_uname
    global sockets_list
    
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
        read_sockets: list[socket.socket]
        exception_sockets: list[socket.socket]

        # Use the select() system call to get a list of sockets which are ready to read
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list, 0.1)
        for notified_socket in read_sockets:
            read_handler(notified_socket)


if __name__ == '__main__':
    Main()
