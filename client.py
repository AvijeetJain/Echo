import socket
import os
import math
import time
import threading

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
                data = file.read(1024)
                if not data:
                    break
                s.send(data)
        print("File sent successfully")
        
    except Exception as e:
        print(f"Error sending file: {e}")
    finally:
        s.close()
        print("Connection closed")

def Main():
    host = '192.168.137.98'  
    port = 4000
    
    server = (host, port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print("Client Connected")
    
    # receive_thread = threading.Thread(target=receive_file, args=(client_socket,))
    # send_thread = threading.Thread(target=send_file, args=(s, client_socket))

    
    # receive_thread.start()
    # send_thread.start()

    # send_thread.join()
    # receive_thread.join()
    send_file(s, server, "hello.txt")
    
if __name__ == '__main__':
    Main()
