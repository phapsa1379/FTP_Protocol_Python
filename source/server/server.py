#pasha ahmadi 9816683
from socket import *
import sys
import time
import os
import struct
import random
curpath1=os.getcwd()
newdir1=curpath1+"\\"+"files"+"\\"
os.chdir(newdir1) 
rootpath=os.getcwd()
print ("\nWelcome to the FTP server.\n\nTo get started, connect a client.")

TCP_IP = "127.0.0.1" 
TCP_PORT = 2121 
BUFFER_SIZE = 1024 
s = socket(AF_INET, SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

def pwd():
    print("pwd..")
    pwd= os.path.relpath(os.curdir,rootpath)
    conn.send(pwd.encode())
    print("Cur dir sent")
def cd():
    flag=0
    print("Cur dir set to :\n")
    conn.send("1".encode())
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if(file_name==".." and os.path.relpath(os.curdir,rootpath)=="." ):
        conn.send("1".encode())
        print("Bad request !!!\n You dont have permition")
        return
    else:
        conn.send("-1".encode())
        flag=1
        

    if os.path.isdir(file_name):
        conn.send(struct.pack("i", 1))
    else:
        conn.send(struct.pack("i", -1))
        print("There is no any folder with this name!!")
        return
    curpath=os.getcwd()
    newdir=curpath+"\\"+file_name+"\\"
    os.chdir(newdir)
    ans=os.path.relpath(os.curdir,rootpath)
    ans=ans.replace("\\","/")
    print("\t"+ans)
    print("new dir sent to client")
    if(flag):
        pwd2= os.path.relpath(os.curdir,rootpath)
        conn.send(pwd2.encode())
    flag=0
    return
    



def list_files():
    print ("Listing files...")
    listing = os.listdir(os.getcwd())
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    for i in listing:
        conn.send(struct.pack("i", sys.getsizeof(i)))
        j=i
        if(os.path.isdir(i)):
            j=">"+j
        conn.send(j.encode())
        
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        conn.recv(BUFFER_SIZE).decode()
    conn.send(struct.pack("i", total_directory_size))
    conn.recv(BUFFER_SIZE).decode()
    print ("Successfully sent file listing")
    return

def dwld():
    conn.send("1".encode())
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    print (file_name_length)
    file_name = conn.recv(file_name_length).decode()
    print (file_name)
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        print ("File name not valid")
        conn.send(struct.pack("i", -1))
        return
    #####################################################
    hostname = "127.0.0.1"
    SP = random.randint(3000,50000)
    conn.sendall(str(SP).encode())
    Fsocket = socket(AF_INET , SOCK_STREAM)
    Fsocket.bind((hostname , SP))
    Fsocket.listen()
    FTPConnection , FTPClientAddress = Fsocket.accept()

    start_time = time.time()

    File = open(file_name , "rb")
    FileContent=File.read()
    File.close()
    FTPConnection.sendall(FileContent)
    FTPConnection.close()
    

    #####################################################
    conn.recv(BUFFER_SIZE).decode()
    print ("Sending file...")
    conn.recv(BUFFER_SIZE).decode()
    conn.send(struct.pack("f", time.time() - start_time))
    return
    


def quit():
    conn.send("1".encode())
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)



  
while True:
    conn, addr = s.accept()
    print ("\nConnected to by address: {}".format(addr))
    while True:
        
        print("*********************************")
        print ("\n\nWaiting for instruction")
        data = conn.recv(BUFFER_SIZE).decode()
        print ("\nRecieved instruction: {}".format(data))
        
        if data=="PWD":
            pwd()
        elif data=="CD":
            cd()
        elif data == "LIST":
            list_files()
        elif data == "DWLD":
            dwld()
        elif data == "QUIT":
            quit()
        if(not data):
            break
        data = None
        
