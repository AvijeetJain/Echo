import socket
import threading


def send_message(address, socket):
    while True:
        message = input("-> ")
        print("Sending: " + message)
        socket.sendto(message.encode('utf-8'), address)

def receive_message(socket):
    while True:
        data, addr = socket.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from: " + str(addr))
        print("From connected user: " + data)


def Main():
    host = '192.168.171.170'  # Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")

    client_address = ('192.168.171.59', 4005)  # Initialize client address


    
    receive_thread = threading.Thread(target=receive_message, args=(s,))
    send_thread = threading.Thread(target=send_message, args=(client_address, s))

    
    receive_thread.start()
    send_thread.start()

    send_thread.join()
    receive_thread.join()

    s.close()

if __name__ == '__main__':
    Main()
