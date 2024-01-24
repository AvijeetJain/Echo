#connected_clients data class with clients ip and socket

class peers:
    def __init__(self, ip, socket):
        self.ip = ip
        self.socket = socket
    
    def get_ip(self):
        return self.ip

    def get_socket(self):
        return self.socket
    