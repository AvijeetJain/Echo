import hashlib
import os
import socket
import time
from client.main import CLIENT_IP

from client.ui.EchoMainWindow import SERVER_ADDR
from utils.constants import HEARTBEAT_TIMER
from utils.types import HeaderCode


class HeartbeatWorker():
    # global SERVER_SOCKET
    # SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # def list_files_and_empty_folders(self, folder_path):
    #     file_list = []

    #     for root, dirs, files in os.walk(folder_path):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             file_list.append(str(file_path))
            
    #         for folder in dirs:
    #             folder_path = os.path.join(root, folder)
    #             file_list.append(str(folder_path))
    #     return file_list
    
    # def to_json(self):
    #     list = self.list_files_and_empty_folders('./public')
    #     tree = {}
    #     for path in list:                
    #         node = tree                   
    #         for level in path.split('\\'): 
    #             if level:                 
    #                 node = node.setdefault(level, dict())
    #     # with open('output.json', 'w') as json_file:
    #     #     json.dump(tree, json_file, indent=2)
    #     return tree
    
    def run(self):
        while True:
            print('CONNECTING TO SERVER')
            SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SERVER_SOCKET.connect(SERVER_ADDR)
            print('CONNECTED TO SERVER') 
            heartbeat = str(HeaderCode.HEARTBEAT) + '@' + CLIENT_IP + '@' + str(self.to_json())
            heartbeat = heartbeat + '@' + hashlib.sha256(heartbeat.encode()).hexdigest()
            SERVER_SOCKET.send(heartbeat.encode('utf-8'))
            
            print("Heartbeat sent")
            time.sleep(HEARTBEAT_TIMER)