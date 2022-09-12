import os.path
import pickle
import socket
import threading
import time

clients = []
files = []
"""
This class represents a Server
"""

class Server:
    def __init__(self):
        #INITING THE SERVER
        self.ip = socket.gethostbyname(socket.gethostname()) # get ip of the server
        while 1:
            try:
                self.port = 10000
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new socket AF_INET = address family , socket type = SOCK_STREAM.
                self.s.bind((self.ip, self.port)) # bind the socket to the port. if the port is already has been socketed it will send error.

                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        files.append('file.txt')
        files.append('largerFile.txt')
        self.filenum = 0
        self.accept_connections()

    def accept_connections(self):
        self.s.listen(100) # maximum client to listen
        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()
            print("Accepted a connection request from %s:%s" % (addr[0], addr[1]));
            self.connections.append(c)
            client_name = c.recv(1024)
            clients.append(client_name.decode())
            #Sending the user the files he can get from the server
            data = 'files'
            for f in files:
                data = f'{data}|{f}'
            self.broadcast(data)
            #2 threads. first one an infinite loop to handle the spasific client, second one is an infinity loop refreshing the users every second
            threading.Thread(target=self.handle_client, args=(c,)).start()
            threading.Thread(target=self.user_update, args=(c,)).start()
    #Userlist update function
    def user_update(self, data):
        while 1:
            time.sleep(1)
            data = "accounts|" + "|".join(clients)
            data = data.encode()
            for client in self.connections:
                try:
                    client.send(data)
                except:
                    pass
    #Sending a messege to all clients
    def broadcast(self, data):
        data = data.encode()
        for client in self.connections:
            try:
                client.send(data)
            except:
                pass
    #Sending a messege to a spasific client
    def pbroadcast(self, data, index):
        data = data.encode()
        client = self.connections.__getitem__(index)
        try:
            client.send(data)
        except:
            pass
    #Sending a file
    def sendFile(self,file,index):
        filePackets = []
        seq = 0
        filesize = os.path.getsize(file)
        sizeToRead = 1000
        if filesize < sizeToRead:
            sizeToRead = 1
        with open(file,'rb',0) as f:
            while True:
                curr = f.read(sizeToRead)
                if not curr:
                    break
                else:
                    currpack = (seq,curr)
                    currpack = pickle.dumps(currpack)
                    filePackets.append(currpack)
                    seq = seq + 1
        newUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        newUDP.bind((self.ip,60000))
        msg, udpaddr = newUDP.recvfrom(1024)
        newUDP.sendto('SYNACK'.encode(), udpaddr)
        msg = newUDP.recvfrom(1024)[0].decode()
        acknum = -1
        if msg == 'ack2':
            z=1
            newUDP.sendto(f'{len(filePackets)}'.encode(), udpaddr)
            while len(filePackets) > 0:
                z+=1
                newUDP.sendto(filePackets[0], udpaddr)
                try:
                    acknum = newUDP.recvfrom(1024)[0].decode()
                except:
                    pass
                acknum = int(acknum)
                curr = pickle.loads(filePackets[0])
                if curr[0] == acknum:
                    filePackets.pop(0)
        else:
            pass
        i = file.index('.')
        filename = f'{file[0:i]}{self.filenum}{file[i:]}'
        newUDP.sendto(filename.encode(),udpaddr)
        self.filenum = self.filenum + 1
        self.pbroadcast(f'{file} was downloaded',index)
        return

    #Infinite loop handling a spasific client
    def handle_client(self, c):
        threadrun = True #If this is false the client disconnected and the thread should be terminated
        while threadrun:
            data = ''
            try:
                data = c.recv(1024)
                #Checking if there is data now
                if data is not None:
                    data = data.decode()
                    #This is a private messege
                    if data[0:2] == 'p.':
                        data = data[2:]
                        i = data.index('.')
                        wispTo = data[0:i]
                        data = data[i+1:]
                        data = f'Private From {data}'
                        self.pbroadcast(data,clients.index(wispTo))
                    #This is a file request
                    elif data[0:8] == 'filereq.':
                        index = self.connections.index(c)
                        data = data[8:]
                        for f in files:
                            if f == data:
                                file = f
                        threading.Thread(target=self.sendFile, args=(file,index)).start()
                    #This is a regular messege
                    else:
                        self.broadcast(data)

            except socket.error:
                i = self.connections.index(c)
                self.connections.remove(c)
                clients.pop(i)
                c.close()
                threadrun = False


server = Server()