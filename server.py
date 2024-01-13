import socket
import threading
import math
import os


def send_file(s, server):
    file_path = input("Enter the path of the file to send: ")

    file_name = file_path.split("/")[-1]
    s.sendto(file_name.encode('utf-8'), server)
    
    file_size = os.path.getsize(file_path)
    file_size = file_size/10240
    s.sendto(str(file_size).encode('utf-8'), server)

    with open(file_path, 'rb+') as file:
        data = file.read(10240)
        
        while data:
            s.sendto(data, server)
            data = file.read(10240)
        file.close()
    print("File sent successfully")

def receive_file(socket):
    file_name, addr = socket.recvfrom(1024)
    file_name = file_name.decode('utf-8').strip()
    print("Receiving file:", file_name)

    file_size, addr = socket.recvfrom(1024)
    file_size = file_size.decode('utf-8').strip()

    file_size = math.ceil(float(file_size))
    print('Blocks of file going to be received: ', file_size)

    with open(file_name, 'wb+') as file:
        for i in range(0,file_size):  
            data, addr = socket.recvfrom(10240)          
            # data = data.decode('utf-8').strip()
            file.write(data)

            print(i/file_size * 100, "% transfer complete")
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


def Main():
    host = '192.168.137.1'  # Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")

    client_address = ('192.168.137.196', 4005)  # Initialize client address
    
    # data, addr = s.recvfrom(1024)
    # client_address = addr

    # send_file(s, client_address)
    # receive_file(s)
    
    receive_thread = threading.Thread(target=receive_file, args=(s,))
    send_thread = threading.Thread(target=send_file, args=(s, client_address))

    
    receive_thread.start()
    send_thread.start()

    send_thread.join()
    receive_thread.join()

    s.close()

if __name__ == '__main__':
    Main()
