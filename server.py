import socket
import threading
import math


def send_file(s, server):
    file_path = input("Enter the path of the file to send: ")

    file_name = file_path.split("/")[-1]
    s.sendto(file_name.encode('utf-8'), server)

    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            s.sendto(data, server)
            data = file.read(1024)
    print("File sent successfully")

def receive_file(socket):
    file_name, addr = socket.recvfrom(1024)
    file_name = file_name.decode('utf-8').strip()
    print("Receiving file:", file_name)

    with open(file_name, 'w') as file:
        data, addr = socket.recvfrom(1024)
        data = data.decode('utf-8').strip()

        print('Blocks of file goint to be received: ', float(data))
        for i in range(0,math.ceil(float(data))):  
            data, addr = socket.recvfrom(1024)          
            data = data.decode('utf-8').strip()
            # data = codecs.decode(data)
            if(data is None):
                print("file ended")
                break
            file.write(data)
                # print("data is :", data, type(data))
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

    receive_file(s)
    send_file(client_address, s)
    
    # receive_thread = threading.Thread(target=receive_message, args=(s,))
    # send_thread = threading.Thread(target=send_message, args=(client_address, s))

    
    # receive_thread.start()
    # send_thread.start()

    # send_thread.join()
    # receive_thread.join()

    s.close()

if __name__ == '__main__':
    Main()
