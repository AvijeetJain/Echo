import socket

def Main():
    host='192.168.137.196' #client ip
    port = 4005
    
    server = ('192.168.68.236', 4000)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    
    message = input("-> ")
    print("sending -> ",message)
    while message !='q':
        s.sendto(message.encode('utf-8'), server)
        s.sendto(message.encode('utf-8'), server)
        s.sendto(message.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)
        message = input("-> ")
    s.close()

if __name__=='__main__':
    Main()

