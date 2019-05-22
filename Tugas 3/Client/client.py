import sys
import socket
import json
import glob

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


def download(namanya):
    print "Request Download", namanya
    sock.sendall("DOWNLOAD")
    sock.sendall(namanya)
    file_data=""
    while True:
        data = sock.recv(200)
        if data=="FINISHED":
            break
        file_data+=data
    fp = open(namanya,'wb+')
    fp.write(file_data)
    fp.close()
    print namanya, "downloaded"


def upload(namanya):
    print "Uploading", namanya
    sock.sendall("UPLOAD")
    sock.sendall(namanya)
    count=0
    kirim=""
    fp = open(namanya,'rb')
    message = fp.read()
    fp.close()
    for x in message:
        kirim+=x
        count+=1
        if count%200==0:
            sock.sendall(kirim)
            kirim=""
        elif count==len(message):
            sock.sendall(kirim)
            sock.sendall("FINISHED")
            break

def menu():
    print "-------------MENU-----------------"
    print "1. Download  : 1 nama_file"
    print "2. Upload    : 2 nama_file"
    print "3. Your list : mylist"
    print "4. Exit      : exit"
    #Tampilan Menu
    jawab = raw_input()
    if jawab=="Exit":
        sock.sendall("EXIT")
        sock.close()
        sys.exit()
    elif jawab =="mylist":
        checkLocalFiles()
    else:
        if jawab[0]=="1":
            namafile=""
            count=0
            for x in jawab:
                if count>1:
                    namafile+=x
                count+=1
            print namafile
            download(namafile)
        elif jawab[0]=="2":
            namafile=""
            count=0
            for x in jawab:
                if count>1:
                    namafile+=x
                count+=1
            print namafile
            upload(namafile)

def checkLocalFiles():
    file_server = []
    file_server.extend(glob.glob('*'))
    print "------------mylist----------------"
    for x in file_server:
        print x

# Terima Data List Directory Server

listdir=""
while True:
    data = sock.recv(200)
    if data=="FINISHED":
        break
    listdir+=data
count=1
print "----------DIRECTORY SERVER------------"
for files in json.loads(listdir):
    print count, files
    count+=1

while True:
    menu()
    