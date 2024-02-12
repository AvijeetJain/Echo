import socket

def recvall(peer_socket: socket.socket, length: int) -> bytes:
    """Utility to ensure lossless reception of data for a large communication.

    The function receives in a loop till the expected amount of data is received.
    This is done prevent data loss, as the socket.recv method by itself cannot guarantee a lossless reception.

    Parameters
    ----------
    peer_socket : socket.socket
        Socket on which to receive data.
    length : int
        Expected size of incoming data.

    Returns
    -------
    bytes
        Returns all the data received by the function.
    """
    received = 0
    data: bytes = b""
    while received != length:
        new_data = peer_socket.recv(length)
        if not len(new_data):
            break
        data += new_data
        received += len(new_data)
    return data