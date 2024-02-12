from enum import Enum
from pydantic import BaseModel
from PyQt5.QtCore import QMutex

class HeaderCode(Enum):
    ERROR = "e"
    DIRECT_TRANSFER_REQUEST = "t"
    DIRECT_TRANSFER = "T"
    FILE_REQUEST = "F"
    FILE_SHARE = "S"
    REQUEST_UNAME = "R"
    MESSAGE = "m"
    NEW_CONNECTION = "n"
    REQUEST_IP = "r"
    HEARTBEAT = "h"
    
# Compression mode to be used
class CompressionMethod(Enum):
    NONE = 0
    ZSTD = 1


# Receiving status of a file
class TransferStatus(Enum):
    NEVER_STARTED = 0
    DOWNLOADING = 1
    PAUSED = 2
    COMPLETED = 3
    FAILED = 4
    

class TransferProgress(BaseModel):
    status: TransferStatus
    progress: int
    percent_progress: float


# Metadata for progress widgets
class ProgressBarData(BaseModel):
    current: int
    total: int


# Data available in a request received by server
class SocketMessage(BaseModel):
    type: HeaderCode
    query: bytes


# Metadata for a file item
class FileMetadata(BaseModel):
    path: str
    size: int
    hash: str | None
    compression: CompressionMethod


# Information sent while requesting a file
class FileRequest(BaseModel):
    filepath: str
    port: int
    request_hash: bool
    resume_offset: int  # If part of file has been received previously


class FileSearchResult(BaseModel):
    uname: str
    filepath: str
    filesize: int
    hash: str


# Directory structure (files and folders) data representation [recursive]
class DirData(BaseModel):
    name: str
    path: str
    type: str
    size: int | None
    hash: str | None
    compression: int
    children: list["DirData"] | None  # type: ignore


# Global search result data
class ItemSearchResult(BaseModel):
    owner: str
    data: DirData


# Hash updation data
class UpdateHashParams(BaseModel):
    filepath: str
    hash: str


# TinyDB document schema
class DBData(BaseModel):
    uname: str
    share: list[DirData]
    

# User settings dictionary/json format
class UserSettings(BaseModel):
    uname: str
    server_ip: str
    share_folder_path: str
    downloads_folder_path: str
    show_notifications: bool


# Chat message object
class Message(BaseModel):
    sender: str
    content: str