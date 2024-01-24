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
        break

def send_chat(client_socket):
    try:
        while True:
            message = input("Enter your message: ")
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending chat message: {e}")
        break

def receive_file(client_socket, download_path):
    try:
        file_name = client_socket.recv(1024).decode('utf-8')
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
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
    
def request_file(client_socket, file_path):
    try:
        file_name = os.path.basename(file_path)
        client_socket.send(file_name.encode('utf-8'))
        print("Requesting file...")
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print("File received")
    except Exception as e:
        print(f"Error requesting file: {e}")
        
def main():
    host = '192.168.0.196'
    port_chat = 5555
    port_file = 5556

    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.bind((host, port_chat))
    chat_socket.listen()

    print(f"Chat server listening on {host}:{port_chat}")

    file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_socket.bind((host, port_file))
    file_socket.listen()

    print(f"File server listening on {host}:{port_file}")

    chat_client, chat_addr = chat_socket.accept()
    file_client, file_addr = file_socket.accept()

    print(f"Chat connection established with {chat_addr}")
    print(f"File connection established with {file_addr}")

    chat_receive_thread = threading.Thread(target=receive_chat, args=(chat_client,))
    chat_send_thread = threading.Thread(target=send_chat, args=(chat_client,))
    file_receive_thread = threading.Thread(target=receive_file, args=(file_client, 'downloads'))
    file_send_thread = threading.Thread(target=send_file, args=(file_client, './Public/hello.txt'))

    chat_receive_thread.start()
    chat_send_thread.start()
    file_receive_thread.start()
    file_send_thread.start()

    # Wait for threads to finish
    chat_receive_thread.join()
    chat_send_thread.join()
    file_receive_thread.join()
    file_send_thread.join()

    # Close sockets
    chat_socket.close()
    file_socket.close()

if __name__ == "__main__":
    main()
