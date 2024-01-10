import socket
import threading

def ip_address():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wi-fi' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()

def send_file(s, server):
    file_path = input("Enter the path of the file to send: ")

    file_name = file_path.split("/")[-1]
    s.sendto(file_name.encode('utf-8'), server)

    with open(file_path, 'r') as file:
        data = file.read(1024)
        while data:
            s.sendto(data.encode('utf-8'), server)
            data = file.read(1024)
        file.close()
    print("File sent successfully")

def receive_file(socket):
    file_name, addr = socket.recvfrom(1024)
    file_name = file_name.decode('utf-8').strip()
    print("Receiving file:", file_name)

    with open(file_name, 'wb') as file:
        while True:
            data, addr = socket.recvfrom(1024)
            if not data:
                break
            file.write(data)

    print("File received successfully")

def Main():
    host = ip_address()
    port = 4005

    server = ('192.168.171.170', 4000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    print("Server Started")
    # send_thread = threading.Thread(target=send_message, args=(s, server))
    # receive_thread = threading.Thread(target=receive_message, args=(s,))

    # send_thread.start()
    # receive_thread.start()

    # send_thread.join()
    # receive_thread.join()
    
    send_file(s, server)
    receive_file(s)

    s.close()

if __name__ == '__main__':
    Main()
