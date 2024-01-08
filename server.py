import socket

def send_message(address, socket):
    message = input("-> ")
    print("Sending: " + message)
    socket.sendto(message.encode('utf-8'), address)

def received_message(data, addr):
    data = data.decode('utf-8')
    print("Received from: " + str(addr))
    print("From connected user: " + data)

def send_ack(address, socket):
    message = "ACK"
    print("Sending: " + message)
    socket.sendto(message.encode('utf-8'), address)


def Main():
   
    host = '192.168.68.236' #Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        received_message(data, addr)
        # data = data.upper()
        send_message(addr, s)
        send_message(addr, s)
    c.close()

if __name__=='__main__':
    Main()
