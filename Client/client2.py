#!/usr/bin/python
# -- coding: utf-8 -- 

import socket
import os
import sys
import select

host = '192.168.137.1'
port = 4000
backlog = 1
size = 4096

#function to send file
def sendf(soc):
    soc.send('file name: ')
    fname = soc.recv(size)    
    fname.decode('utf-8')
    file=open(fname,'rb')
    data=file.read()
    data.encode('utf-8')
    soc.send(data)
    print ('File sent')

#function to receive file
def recvf(soc):
    data = soc.recv(size)
    user_input = input(data.decode('utf-8'))
    soc.send(user_input.encode('utf-8'))
    data = soc.recv(40960)
    data.decode('utf-8')
    if user_input.endswith('.txt'):
        file=open('abc.txt','w')
    elif user_input.endswith('.pdf'):
        file=open('abc.pdf','w')
    elif user_input.endswith('.png'):
        file=open('abc.png','w')
    file.write(str(data))
    file.close()
    print ('File received')

#function for client to listen for other client connections
def clisten(user_input):
    cport = int(user_input)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #binding the socket to localhost and port
    s.bind((host,cport))
    print ('listening')
    s.listen(backlog)
    clist=[s]
    while 1:
    # Using Select to handle multiplexing
        inready,outready,exceptready = select.select(clist,[],[])
        for sock in inready:
            if sock == s:
                client, address = s.accept()
                clist.append(client)
                print ('connected')
                client.send('Start typing')
            else:
                try:
                    data = sock.recv(size)
                    data.decode('utf-8')
                    if data:
                        print (data)
                        if data == '\SEND_FILE':
                            sendf(client)
                        if data == '\CLOSE_SESSION':
                            print ('session ended')
                            client.close()
                            break
                        user_input = input('<Me> ')
                        user_input.encode('utf-8')
                        client.send(user_input)
                        if user_input == '\SEND_FILE':
                            recvf(client)     
                        if user_input == '\CLOSE_SESSION':
                            print ('session ended')
                            client.close()
                            break
                except:
                    client.close()
                    input.remove(client)
                    #continue                
    return             

#function for client to connect to listening client                
def cconnect(data):
    cport = int(data)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        soc.connect((host,cport))
    except:
        print ('Unable to connect to client')
    print ('now connected')
    while 1:
        data = soc.recv(size)
        data.decode('utf-8')
        print( data)
        if data == '\SEND_FILE':
            sendf(soc)
        if data == '\CLOSE_SESSION':
            print ('session ended')
            soc.close()
            break
        user_input = input('<Me> ')
        soc.send(user_input)
        if user_input == '\SEND_FILE':
            recvf(soc)  
        if user_input == '\CLOSE_SESSION':
            print( 'session ended')
            soc.close()
            break
    return

#main to handle connection between server and client
def main():
    #creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.connect((host,port))
    except:
        print ('Unable to connect to chat server')
        sys.exit()
    while 1:
        data = sock.recv(size)
        data.decode('utf-8')
        if data.isdigit() and int(data)>2000:
            cconnect(data)
        user_input = input(data)
        sock.send(user_input.encode('utf-8'))
        if user_input.isdigit() and int(user_input)>2000:
            clisten(user_input)
        if user_input == '\DISCONNECT_CLIENT':
            sock.close()
            break

if __name__ == '__main__':
    sys.exit(main()) 