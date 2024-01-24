import socket
import threading
import time
import math
import os
from utils.data.peers import peers

# files = ['test_server.py']

def send_file(s, server):
    try:
        file_path = input("Enter the path of the file to send: ")
        file_name = file_path.split("/")[-1]
        print("Sending file:", file_name)
        s.send(file_name.encode())

        file_size = os.path.getsize(file_path)
        file_size = str(math.ceil(file_size/1024))
        print("File size is:", file_size)

        s.send(file_size.encode())
        #delay 1 sec
        time.sleep(1)

        with open(file_path, 'rb') as file:
            while True:
                data = file.read(10240)
                if not data:
                    break
                s.send(data)
        print("File sent successfully")
        
    except Exception as e:
        print(f"Error sending file: {e}")

def receive_file(socket):
    file_name = socket.recv(1024)
    file_name = file_name.decode().strip()
    print("Receiving file:", file_name)

    file_size = socket.recv(1024)
    file_size = file_size.decode().strip()

    file_size = int(file_size)
    print('Blocks of file going to be received: ', file_size)

    with open(file_name, 'wb') as file:
        data = socket.recv(10240) 
        i = 0 
        while data:          
            # data = data.decode('utf-8').strip()
            file.write(data)
            data = socket.recv(10240) 

            print(i/file_size * 100, "% transfer complete")
            i += 1
    file.close()
    print("File received successfully")

# def send_message(address, socket):
#     while True:
#         message = input("-> ")
#         print("Sending: " + message)
#         socket.sendto(message.encode('utf-8'), address)

# def receive_message(socket):
#     while True:
#         data, addr = socket.recvfrom(1024)
#         data = data.decode('utf-8')
#         print("Received from: " + str(addr))
#         print("From connected user: " + data)

# function to start server and connect to 10 clients and return list of ip addresses of clients
def start_server():
    host = ''
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)

    connected_peers = []

    for i in range(10):
        client_socket, addr = s.accept()
        connected_peers.append(peers(addr, client_socket))

    print("Server Started")

    return connected_peers


def Main():
    host = '192.168.137.1'  # Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    client_socket, addr = s.accept()

    print("Server Started")

    client_address = ('192.168.137.231', 4005)  # Initialize client address
    
    # data, addr = s.recvfrom(1024)
    # client_address = addr

    send_file(s, client_address)
    # receive_file(client_socket)
    
    # receive_thread = threading.Thread(target=receive_file, args=(client_socket,))
    # send_thread = threading.Thread(target=send_file, args=(s, client_socket))

    
    # receive_thread.start()

    # send_thread.join()
    # receive_thread.join()

    # Close the socket after all files are sent
    s.close()

if __name__ == '__main__':
    Main()
