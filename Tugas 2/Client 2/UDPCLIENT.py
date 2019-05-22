import socket
import base64
import os
import sys
import glob

TARGET_IP = '127.0.0.1'
TARGET_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Connect Server
sock.sendto('CONNECT',(TARGET_IP, TARGET_PORT))
print "Connecting to Server", TARGET_IP, TARGET_PORT

#Receive Server Response
data, addr = sock.recvfrom(1024)
if data == "CONNECT":
    print "Connected to", addr

while True:
    data, addr = sock.recvfrom(1024)
    if data == "START":
        IMAGENAME, addr = sock.recvfrom(1024)
        print "Download", IMAGENAME
        fp = open(IMAGENAME,'wb+')
        terimadata=""
        while True:
            data, addr = sock.recvfrom(1024)
            terimadata+=data
            if data=="FINISH":
                break
        fp.write(terimadata)
        fp.close()
        print "Download Success"
            


# namafile='pasfoto.jpg'
# ukuran = os.stat(namafile).st_size


# fp = open('pasfoto.jpg','rb')
# k = fp.read()
# terkirim=0
# count=0
# kirim=""
# for x in k:
#    kirim+=x
#    count+=1
#    if count%200==0:
#       sock.sendto(kirim, (TARGET_IP, TARGET_PORT))
#       print kirim[0]
#       kirim=""
#    elif count==len(k):
#       print kirim[0]
#       sock.sendto(kirim, (TARGET_IP, TARGET_PORT))
#       sock.sendto("SELESAI", (TARGET_IP, TARGET_PORT))
#       break
#    # terkirim = terkirim + 1
#    # print "\r terkirim {} of {} " . format(terkirim,ukuran)

sys.exit()