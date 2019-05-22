import socket
import base64
import sys
import os
import glob
from threading import Thread
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

def sendImages(IP,PORT,IMAGENAME):
    print "Sending", IMAGENAME, "to", IP, PORT
    sock.sendto("START",(IP,PORT))
    sock.sendto(IMAGENAME,(IP,PORT))
    fp = open(IMAGENAME,'rb')
    k = fp.read()
    count=0
    kirim=""
    for x in k:
        kirim+=x
        count+=1
        if count%200==0:
            sock.sendto(kirim, (IP,PORT))
            kirim=""
        elif count==len(k):
            sock.sendto(kirim, (IP,PORT))
            sock.sendto("FINISH", (IP,PORT))
            break
    print "Send", IMAGENAME, "to", IP,PORT, "Success!"

#Check Local File
def checkLocalImages():
    image = []
    image.extend(glob.glob('*.jpg'))
    image.extend(glob.glob('*.png'))
    return image

#Checking Image
def checkImages(IP,PORT):
    while True:
        image = checkLocalImages()
        for file in image:
            sendImages(IP,PORT,file)
        time.sleep(300)
        
#Main
while True:
    data, addr = sock.recvfrom(1024)
    if data == "CONNECT":
        print "Connected to", addr
        sock.sendto('CONNECT',(addr[0], addr[1]))
        thread = Thread(target=checkImages,args=addr)
        thread.start()





