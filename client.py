import socket
import os
import math
import time
import threading

files= ['AboutTime.zip']

def send_file(s, server, file_path):
    try:
        # file_path = input("Enter the path of the file to send: ")
        file_name = file_path.split("/")[-1]
        s.send(file_name.encode())
        print("Sending file:", file_name)

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
        print(f"Error sending file: {e}")
    # finally:
    #     s.close()
    #     print("Connection closed")
        
def receive_file(socket):
    file_name = socket.recv(1024)
    file_name = file_name.decode().strip()
    print("Receiving file:", file_name)

    file_size = socket.recv(1024)
    file_size = file_size.decode().strip()

    file_size = int(file_size)
    print('Blocks of file going to be received: ', file_size)

    with open(file_name, 'wb') as file:
        data = socket.recv(1024) 
        i = 0 
        while data:          
            # data = data.decode('utf-8').strip()
            file.write(data)
            data = socket.recv(1024) 

            print(i/file_size * 100, "% transfer complete")
            i += 1
    file.close()
    print("File received successfully")

def Main():
    host = '192.168.137.1'  
    port = 4005
    
    server = ('192.168.137.188', 4000)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind((host, port))
    s.connect(server)

    print("Client Connected")
    
    # receive_thread = threading.Thread(target=receive_file, args=(server,))
    # send_thread = threading.Thread(target=send_file, args=(s, server))

    # send_thread.start()
    # receive_thread.start()

    # send_thread.join()
    # receive_thread.join()
    for file_path in files:
        send_thread = threading.Thread(target=send_file, args=(s, server, file_path))
        # receive_thread = threading.Thread(target=receive_file, args=(s,))

        send_thread.start()
        # receive_thread.start()

        send_thread.join()
        time.sleep(1)
        # receive_thread.join()
    
    # send_file(s, server, "hello.txt")
    
if __name__ == '__main__':
    Main()
