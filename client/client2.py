import socket
import threading
import os

def receive_chat(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message: {message}")
    except Exception as e:
        print(f"Error receiving chat message: {e}") 

def send_chat(client_socket):
    
    try:
        while True:
            message = input("Enter your message: ")
            client_socket.send(message.encode('utf-8'))
            
            type = message.split('@')[0]
            if(type == 'download'):
                receive_file( 'downloads')
    except Exception as e:
        print(f"Error sending chat message: {e}") 
        
        

def receive_file( download_path):
    host = '192.168.0.192'
    port_file = 5556
    file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # file_socket.bind((host, port_file))
    # file_socket.listen(1)
    
    file_socket.connect(('192.168.0.196', 5556))
    
    # print(f"File server listening on {host}:{port_file}")
    print('File server connected')
    
    try:
        file_name = file_socket.recv(1024).decode('utf-8')
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'wb') as file:
            while True:
                data = file_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"File received and saved at: {file_path}")
    except Exception as e:
        print(f"Error receiving file: {e}")
    

def send_file(client_socket, file_path):
    try:
        file_name = os.path.basename(file_path)
        client_socket.send(file_name.encode('utf-8'))
        print("Sending file...")
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
        print("File sent")
    except Exception as e:
        print(f"Error sending file: {e}")

def main():
    host = '192.168.0.192'
    port_chat = 5555
    port_file = 5556

    receiver_ip = '192.168.0.196'

    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # chat_socket.bind((host, port_chat))
    # chat_socket.listen()

    print(f"Chat server listening on {host}:{port_chat}")

    # file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # file_socket.bind((host, port_file))
    # file_socket.listen()

    # print(f"File server listening on {host}:{port_file}")


    try:
        chat_server = (receiver_ip, port_chat)
        chat_socket.connect(chat_server)
    except Exception as e:
        print(f"Error connecting to chat server: {e}")


    # try:
    #     file_server = (receiver_ip, 5556)
    #     file_socket.connect(file_server) 
    # except Exception as e:
    #     print(f"Error connecting to file server: {e}")

    # chat_socket, chat_addr = chat_socket.accept()
    # file_socket, file_addr = file_socket.accept()

    # print(f"Chat connection established with {chat_addr}")
    # print(f"File connection established with {file_addr}")

    chat_receive_thread = threading.Thread(target=receive_chat, args=(chat_socket,))
    chat_send_thread = threading.Thread(target=send_chat, args=(chat_socket,))
    # file_receive_thread = threading.Thread(target=receive_file, args=(file_socket, 'downloads'))
    # file_send_thread = threading.Thread(target=send_file, args=(file_socket, './public/Resume.pdf'))

    chat_receive_thread.start()
    chat_send_thread.start()
    # file_receive_thread.start()
    # file_send_thread.start()

    chat_receive_thread.join()
    chat_send_thread.join()
    # file_receive_thread.join()
    # file_send_thread.join()

    chat_socket.close()
    # file_socket.close()

if __name__ == "__main__":
    main()