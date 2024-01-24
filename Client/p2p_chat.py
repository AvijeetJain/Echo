import socket
import threading

def receive_messages(peer_socket, peer_address):
    try:
        while True:
            data = peer_socket.recv(1024).decode('utf-8')
            print(f"Received from {peer_address}: {data}")
    except Exception as e:
        print(f"Error receiving msg: {e}")

def send_messages(peer_socket):
    try:
        while True:
            message = input("-> ")
            peer_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending msg: {e}")

def establish_connection(peer_address, local_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', local_port))
    s.connect(peer_address)
    print("Connection Established")
    return s

def start_p2p_chat(peer_address, local_port):
    peer_socket = establish_connection(peer_address, local_port)

    receive_thread = threading.Thread(target=receive_messages, args=(peer_socket, peer_address))
    send_thread = threading.Thread(target=send_messages, args=(peer_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

if __name__ == '__main__':
    local_port = 5000  # Adjust the local port for each peer

    # Example peer addresses (replace with actual addresses)
    peer1_address = ('192.168.0.192', 5000)
    peer2_address = ('192.168.0.196', 5000)

    # Start P2P chat for each peer
    threading.Thread(target=start_p2p_chat, args=(peer1_address, local_port)).start()
    threading.Thread(target=start_p2p_chat, args=(peer2_address, local_port)).start()
