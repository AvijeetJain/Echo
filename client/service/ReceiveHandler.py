import logging
from pathlib import Path
import select
import socket
import msgpack
from notifypy import Notify
from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
    QThreadPool,
    QThread,
)
from requests import RequestException
from client.ui.EchoMainWindow import show_error_dialog

from utils.constants import FILE_BUFFER_LEN, FMT, HEADER_MSG_LEN, HEADER_TYPE_LEN
from utils.exceptions import ExceptionCode
from utils.helpers import get_unique_filename, path_to_dict
from utils.socket_functions import recvall
from utils.types import FileMetadata, FileRequest, HeaderCode, Message

class ReceiveHandler(QObject):
    """A worker that handles incoming packets sent by connected peers

    Attributes
    ----------
    message_received : pyqtSignal
        A signal that is emitted every time a message is received from a peer
    file_incoming : pyqtSignal
        A signal that is emitted every time a file is being received from a peer
    send_file_pool : QThreadPool
        The global thread pool used to run SendFileWorker instances

    Methods
    -------
    receive_msg(socket: socket.socket)
        Handle receiving incoming file requests, messages and Direct Transfer requests
    run()
        Accept new incoming connections from peers and execute receive_msg for each peer
    """

    message_received = pyqtSignal(dict)
    file_incoming = pyqtSignal(tuple)
    send_file_pool = QThreadPool.globalInstance()

    def receive_msg(self, socket: socket.socket) -> str | None:
        """Receives incoming messages, file requests or Direct Transfer requests

        Parameters
        ----------
        socket : socket.socket
            The socket on which to receive the message

        Returns
        ----------
        str | None
            Returns the message received from the peer, or None in case of an exception

        Raises
        ----------
        RequestException
            In case of any exceptions that occur in receiving the message
        """

        global client_send_socket
        global user_settings

        # Receive message type
        logging.debug(f"Receiving from {socket.getpeername()}")
        message_type = socket.recv(HEADER_TYPE_LEN).decode(FMT)
        if not len(message_type):
            raise RequestException(
                msg=f"Peer at {socket.getpeername()} closed the connection",
                code=ExceptionCode.DISCONNECT,
            )
        elif message_type not in [
            HeaderCode.MESSAGE.value,
            HeaderCode.DIRECT_TRANSFER.value,
            HeaderCode.DIRECT_TRANSFER_REQUEST.value,
            HeaderCode.FILE_REQUEST.value,
        ]:
            raise RequestException(
                msg=f"Invalid message type in header. Received [{message_type}]",
                code=ExceptionCode.INVALID_HEADER,
            )
        else:
            match message_type:
                # Direct Transfer
                case HeaderCode.DIRECT_TRANSFER.value:
                    # Receive file metadata
                    file_header_len = int(socket.recv(HEADER_MSG_LEN).decode(FMT))
                    file_header: FileMetadata = msgpack.unpackb(socket.recv(file_header_len))
                    logging.debug(msg=f"receiving file with metadata {file_header}")

                    # Final path to store the file in
                    write_path: Path = get_unique_filename(
                        Path(user_settings["downloads_folder_path"]) / file_header["path"],
                    )
                    try:
                        file_to_write = open(str(write_path), "wb")
                        logging.debug(f"Creating and writing to {write_path}")
                        try:
                            byte_count = 0

                            # Keep receiving file chunks until the entire file is received
                            while byte_count != file_header["size"]:
                                file_bytes_read: bytes = socket.recv(FILE_BUFFER_LEN)
                                byte_count += len(file_bytes_read)
                                file_to_write.write(file_bytes_read)
                            file_to_write.close()
                            return f"Received file {write_path.name}"
                        except Exception as e:
                            logging.exception(e)
                            # TODO: add status bar message here, show error in progress bar
                            return None
                    except Exception as e:
                        logging.exception(e)
                        # TODO: add status bar message here, show error in progress bar
                        return None
                # Incoming file request
                case HeaderCode.FILE_REQUEST.value:
                    # Receive file request
                    req_header_len = int(socket.recv(HEADER_MSG_LEN).decode(FMT))
                    file_req_header: FileRequest = msgpack.unpackb(socket.recv(req_header_len))
                    logging.debug(msg=f"Received request: {file_req_header}")
                    requested_file_path = Path(user_settings["share_folder_path"]) / file_req_header["filepath"]

                    # Check if the requested file exists and is a file
                    if requested_file_path.is_file():
                        socket.send(HeaderCode.FILE_REQUEST.value.encode(FMT))

                        # Spawn new HandleFileRequestWorker worker to transmit the file
                        send_file_handler = HandleFileRequestWorker(
                            requested_file_path,
                            (socket.getpeername()[0], file_req_header["port"]),
                            file_req_header["request_hash"],
                            file_req_header["resume_offset"],
                        )
                        self.send_file_pool.start(send_file_handler, QThread.HighPriority)  # type: ignore
                        return None
                    # If the requested file exists and is a directory
                    elif requested_file_path.is_dir():
                        raise RequestException(
                            f"Requested a directory, {file_req_header['filepath']} is not a file.",
                            ExceptionCode.BAD_REQUEST,
                        )
                    # If the requested file does not exist
                    else:
                        # Update the share data on the server again with the latest information
                        share_data = msgpack.packb(
                            path_to_dict(
                                Path(user_settings["share_folder_path"]),
                                user_settings["share_folder_path"],
                            )["children"]
                        )
                        share_data_header = f"{HeaderCode.SHARE_DATA.value}{len(share_data):<{HEADER_MSG_LEN}}".encode(
                            FMT
                        )
                        server_socket_mutex.lock()
                        client_send_socket.sendall(share_data_header + share_data)
                        server_socket_mutex.unlock()
                        raise RequestException(
                            f"Requested file {file_req_header['filepath']} is not available",
                            ExceptionCode.NOT_FOUND,
                        )
                # Incoming Direct Transfer request
                case HeaderCode.DIRECT_TRANSFER_REQUEST.value:
                    metadata_len = int(socket.recv(HEADER_MSG_LEN).decode(FMT))
                    metadata: FileMetadata = msgpack.unpackb(socket.recv(metadata_len))
                    # Emit the file_incoming signal
                    self.file_incoming.emit((metadata, socket))
                    return None
                # Incoming message
                case _:
                    message_len = int(socket.recv(HEADER_MSG_LEN).decode(FMT))
                    # Return the received message
                    return recvall(socket, message_len).decode(FMT)

    def run(self):
        """Receives new connections and handles them"""

        global messages_store
        global client_send_socket
        global client_recv_socket
        global connected
        global server_socket_mutex

        while True:
            read_sockets: list[socket.socket]
            # Use the select system call to get a list of sockets that are ready for receiving
            read_sockets, _, __ = select.select(connected, [], [])
            for notified_socket in read_sockets:
                # New incoming connection
                if notified_socket == client_recv_socket:
                    # Accept the connection
                    peer_socket, peer_addr = client_recv_socket.accept()
                    logging.debug(
                        msg=f"Accepted new connection from {peer_addr[0]}:{peer_addr[1]}",
                    )
                    try:
                        # Lookup the username of the peer in the cache
                        if ip_to_uname.get(peer_addr[0]) is None:
                            # In case of a cache miss, lookup the username from the server
                            server_socket_mutex.lock()
                            peer_uname = request_uname(peer_addr[0], client_send_socket)
                            server_socket_mutex.unlock()
                            if peer_uname is not None:
                                # Cache the username for future use
                                ip_to_uname[peer_addr[0]] = peer_uname
                        # Add the socket to the list of connected peers
                        connected.append(peer_socket)
                    except Exception as e:
                        logging.exception(msg=e)
                        show_error_dialog("Error occured when obtaining peer data. {e}")
                        break
                else:
                    # Incoming packet from a connected peer
                    try:
                        # Lookup the username in the cache
                        username = ip_to_uname[notified_socket.getpeername()[0]]
                        # Handle the incoming packet
                        message_content: str = self.receive_msg(notified_socket)
                        # If receive_msg returns a string, it is a message to be displayed in the message area
                        if message_content:
                            message: Message = {"sender": username, "content": message_content}
                            # Check if desktop notifications are enabled in the settings
                            if user_settings["show_notifications"] and username != selected_uname:
                                # Fire a notification with the message as the payload
                                notif = Notify()
                                notif.application_name = "Drizzle"
                                notif.title = "Message"
                                notif.message = f"{username}: {message_content}"
                                notif.send()
                            # Store the message in the messages_store
                            messages_store.setdefault(username, []).append(message)
                            # Emit the message_received signal to update the message area
                            self.message_received.emit(message)
                    except RequestException as e:
                        # Remove disconnected peers from the list of connected peers
                        if e.code == ExceptionCode.DISCONNECT:
                            try:
                                connected.remove(notified_socket)
                            except ValueError:
                                logging.info("already removed")
                        logging.error(msg=f"Exception: {e.msg}")
                        # show_error_dialog(f"Error occurred when communicating with peer.\n{e.msg}")
                        break
                    except Exception as e:
                        logging.exception(f"Error communicating with peer: {e}")