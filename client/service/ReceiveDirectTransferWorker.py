import hashlib
import logging
from pathlib import Path
import shutil
import socket
from PyQt5.QtCore import (
    QRunnable
)
from service import Signals
from ui.errorDialog.ShowErrorDialog import show_error_dialog
from utils.constants import DIRECT_TEMP_FOLDER_PATH, FILE_BUFFER_LEN
from utils.helpers import get_unique_filename

from utils.types import FileMetadata, TransferStatus

class ReceiveDirectTransferWorker(QRunnable):
    """A worker that receives files sent via Direct Transfer from a peer

    Attributes
    ----------
    metadata : FileMetadata
        The metadata of the file to be downloaded
    sender : str
        The username of the sender
    file_receive_socket : socket.socket
        The socket on which to receive the file

    Methods
    -------
    run()
        Receives the file from the sender on the file_receive_socket socket
    """

    def __init__(self, metadata: FileMetadata, sender: str, file_receive_socket: socket.socket):
        super().__init__()
        logging.debug("file recv worker init")
        self.metadata = metadata
        self.sender = sender
        self.file_recv_socket = file_receive_socket
        self.signals = Signals()

    def run(self):
        """Receives the file with the given metadata from the sender on the file_receive_socket socket"""
        global user_settings
        global transfer_progress

        try:
            # Accept connection from the sender
            sender, _ = self.file_recv_socket.accept()
            # Temporary path to write the file to while the download is not complete
            temp_path: Path = DIRECT_TEMP_FOLDER_PATH / self.sender / self.metadata["path"]
            # Final download path in the user's download folder to move the file to after the download is complete
            final_download_path: Path = get_unique_filename(
                Path(user_settings["downloads_folder_path"]) / self.sender / self.metadata["path"],
            )
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            final_download_path.parent.mkdir(parents=True, exist_ok=True)

            # Initialize transfer progress with default values
            transfer_progress[temp_path] = {
                "status": TransferStatus.DOWNLOADING,
                "progress": 0,
                "percent_progress": 0.0,
            }

            logging.debug(msg="Obtaining file")
            # Check if there is sufficient disk space available to receive the file
            if shutil.disk_usage(user_settings["downloads_folder_path"]).free > self.metadata["size"]:
                with temp_path.open(mode="wb") as file_to_write:
                    byte_count = 0
                    hash = hashlib.sha1()
                    self.signals.receiving_new_file.emit((temp_path, self.metadata["size"], False))
                    while True:
                        logging.debug(msg="Obtaining file chunk")

                        # Receive a file chunk
                        file_bytes_read: bytes = sender.recv(FILE_BUFFER_LEN)

                        # Update cumulative file hash
                        hash.update(file_bytes_read)
                        num_bytes_read = len(file_bytes_read)
                        byte_count += num_bytes_read
                        transfer_progress[temp_path]["progress"] = byte_count

                        # Write chunk to temp file
                        file_to_write.write(file_bytes_read)

                        # Emit a signal to update the progress bar
                        self.signals.file_progress_update.emit(temp_path)

                        # If there are no more chunks being sent, terminate the transfer
                        if num_bytes_read == 0:
                            break

                    received_hash = hash.hexdigest()
                    # Compare hash of received file with hash given in the metadata
                    if received_hash == self.metadata["hash"]:
                        transfer_progress[temp_path]["status"] = TransferStatus.COMPLETED
                        final_download_path.parent.mkdir(parents=True, exist_ok=True)

                        # Move the file to the final download path in the user's download folder
                        shutil.move(temp_path, final_download_path)
                        print("Succesfully received 1 file")

                        # Emit a signal to delete the progress bar
                        self.signals.file_download_complete.emit(temp_path)
                        del transfer_progress[temp_path]
                    else:
                        transfer_progress[temp_path]["status"] = TransferStatus.FAILED
                        logging.error(msg=f"Failed integrity check for file {self.metadata['path']}")
                        show_error_dialog(f"Failed integrity check for file {self.metadata['path']}.")
        except Exception as e:
            logging.exception(msg=f"Failed to receive file: {e}")
            show_error_dialog(f"Failed to receive file: {e}")
        finally:
            # Close the connection with the sender
            self.file_recv_socket.close()