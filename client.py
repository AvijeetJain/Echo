# # Import socket module 
# import socket			 

# # Create a socket object 
# s = socket.socket()		 

# # Define the port on which you want to connect 
# port = 12345			

# # connect to the server on local computer 
# s.connect(('', port)) 

# # receive data from the server and decoding to get the string.
# print (s.recv(1024).decode())
# # close the connection 
# s.close()	 
	

# import socket

# def Main():
#     host='192.168.137.196' #client ip
#     port = 4005
    
#     server = ('192.168.68.236', 4000)
    
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind((host,port))
    
#     message = input("-> ")
#     print("sending -> ",message)
#     while message !='q':
#         s.sendto(message.encode('utf-8'), server)
#         s.sendto(message.encode('utf-8'), server)
#         s.sendto(message.encode('utf-8'), server)
#         data, addr = s.recvfrom(1024)
#         data = data.decode('utf-8')
#         print("Received from server: " + data)
#         message = input("-> ")
#     s.close()

# if __name__=='__main__':
#     Main()



import socket
import threading

def send_message(s, server):
    while True:
        message = input("-> ")
        print("sending -> ", message)
        s.sendto(message.encode('utf-8'), server)

def receive_message(s):
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print(str(addr))
        print("Received from server: "+ data)

def Main():
    host = '192.168.171.59'  # client ip
    port = 4005

    server = ('192.168.171.170', 4000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    send_thread = threading.Thread(target=send_message, args=(s, server))
    receive_thread = threading.Thread(target=receive_message, args=(s,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    s.close()

if __name__ == '__main__':
    Main()
