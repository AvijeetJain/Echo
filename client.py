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
    host = ip_address()
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
