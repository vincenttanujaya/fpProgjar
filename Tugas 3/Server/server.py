import sys
import socket
import glob
import json
from threading import Thread


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

def receive(connection):
    namafile, addr = connection.recvfrom(1024)
    datafile=""
    print "downloading ", namafile
    while True:
        data = connection.recv(200)
        if data=="FINISHED":
            break
        datafile+=data
    fp = open(namafile,'wb+')
    fp.write(datafile)
    fp.close()
    print namafile, "downloaded"

def send(connection):
    namafile, addr = connection.recvfrom(1024)
    print "Sending ", namafile
    fp = open(namafile,'rb')
    message = fp.read()
    fp.close()
    sendFile(message,connection)

def sendFile(message,connection):
    count=0
    kirim=""
    for x in message:
        kirim+=x
        count+=1
        if count%200==0:
            connection.sendall(kirim)
            kirim=""
        elif count==len(message):
            connection.sendall(kirim)
            connection.sendall("FINISHED")
            break

#Cek File Lokal
def checkLocalFiles():
    file_server = []
    file_server.extend(glob.glob('*'))
    return file_server

#Menu Utama
def menuUtama(IP,PORT,connection):
    files = json.dumps(checkLocalFiles())
    sendFile(files,connection)
    while True:
        feedback, addr = connection.recvfrom(1024)
        if feedback == "UPLOAD":
            receive(connection)
        elif feedback == "DOWNLOAD":
            send(connection)
        elif feedback == "EXIT":
            print "Disconnected", IP
            break
    

print 'Waiting for a connection...'

while True:
    connection, client_address = sock.accept()
    print 'Receive Connection from', client_address
    thread = Thread(target=menuUtama,args=(client_address[0],client_address[1],connection))
    thread.start()





        