import socket
import threading
import os

def receive_chat(socket_socket):
    while True:
        try:
            message = socket_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message: {message}")
        except Exception as e:
            print(f"Error receiving chat message: {e}")
            break

def send_chat(socket_socket):
    while True:
        message = input("Enter your message: ")
        try:
            socket_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending chat message: {e}")
            break

def receive_file(socket_socket):
    file_name = socket_socket.recv(1024).decode('utf-8')
    try:
        with open(file_name, 'wb') as file:
            while True:
                data = socket_socket.recv(1024)
                if not data:
                    break
                file.write(data)
    except Exception as e:
        print(f"Error receiving file: {e}")

def send_file(socket_socket, file_path):
    file_name = os.path.basename(file_path)
    try:
        socket_socket.send(file_name.encode('utf-8'))
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                socket_socket.send(data)
    except Exception as e:
        print(f"Error sending file: {e}")

def main():
    host = '192.168.137.231'
    port_chat = 5555
    port_file = 5556

    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # chat_socket.bind((host, port_chat))
    # chat_socket.listen()

    print(f"Chat server listening on {host}:{port_chat}")

    file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # file_socket.bind((host, port_file))
    # file_socket.listen()

    print(f"File server listening on {host}:{port_file}")
    
    chat_server = ('192.168.137.1', 5555)
    chat_socket.connect(chat_server)
    
    
    
    file_server = ('192.168.137.1', 5556)
    file_socket.connect(file_server)   

    # chat_socket, chat_addr = chat_socket.accept()
    # file_socket, file_addr = file_socket.accept()

    # print(f"Chat connection established with {chat_addr}")
    # print(f"File connection established with {file_addr}")

    chat_receive_thread = threading.Thread(target=receive_chat, args=(chat_socket,))
    chat_send_thread = threading.Thread(target=send_chat, args=(chat_socket,))
    file_receive_thread = threading.Thread(target=receive_file, args=(file_socket,))
    file_send_thread = threading.Thread(target=send_file, args=(file_socket, 'NikhilResume.pdf'))

    chat_receive_thread.start()
    chat_send_thread.start()
    file_receive_thread.start()
    file_send_thread.start()

    chat_receive_thread.join()
    chat_send_thread.join()
    file_receive_thread.join()
    file_send_thread.join()

    chat_socket.close()
    file_socket.close()

if __name__ == "__main__":
    main()