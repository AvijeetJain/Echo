from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal

class Signals(QObject):
    """A class containing signals that are emitted for various events

    Attributes
    ----------
    start_download : pyqtSignal
        A signal that is emitted when a download starts from the search dialog, to create a progress bar
    receiving_new_file : pyqtSignal
        A signal that is emitted when the a new file download starts, to create a progress bar
    file_progress_update : pyqtSignal
        A signal that is emitted when a file transfer progress is updated, to update the progress bar
    dir_progress_update : pyqtSignal
        A signal that is emitted when a directory transfer progress is updated, to update the progress bar
    pause_download : pyqtSignal
        A signal that is emitted when a file or directory transfer is paused
    resume_download : pyqtSignal
        A signal that is emitted when a file or directory transfer is resumed
    file_download_complete : pyqtSignal
        A signal that is emitted when a file or directory transfer is completed
    """

    dir_progress_update = pyqtSignal(tuple)
    file_download_complete = pyqtSignal(Path)
    file_progress_update = pyqtSignal(Path)
    pause_download = pyqtSignal(Path)
    receiving_new_file = pyqtSignal(tuple)
    resume_download = pyqtSignal(Path)
    start_download = pyqtSignal(dict)