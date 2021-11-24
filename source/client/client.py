#pasha ahmadi 9816683
from socket import *
import sys
import os
import struct

TCP_IP = "127.0.0.1" 
TCP_PORT = 2121 
BUFFER_SIZE = 1024 
s = socket(AF_INET, SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

def help():
    print("\n\nWelcome to the FTP client. ")
    print("Call one of following functions : \n")
    print("HELP                  : Show this help")
    print("LIST                  : List files")
    print("PWD                   : Show current dir")
    print("CD dir_name           : Change directory")
    print("DWLD file_path        : Download file")
    print("QUIT                  : Exit\n")


def cd(folder_name):
    print ("Changing dir to: {}...".format(folder_name))
    flag=0
    try:
        s.send("CD".encode())
        s.recv(BUFFER_SIZE).decode()
    except:
        print ("Couldn't connect to server. Make sure a connection has been established.")
        return
    try:
        s.send(struct.pack("h", sys.getsizeof(folder_name)))
        s.send(folder_name.encode())
        pg=s.recv(BUFFER_SIZE).decode()
        if(pg=="1"):
            print("Now you are in root folder and you dont have permition to go back from root folder!!")
            return
        else:
            flag=1
              
    except:
        print ("Couldn't send folder details")
        return

    try:
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == -1:
            print ("The folder does not exist on server")
            return
    except:
        print ("Couldn't determine folder existance")
        return
    if(flag):
        answer11= s.recv(BUFFER_SIZE).decode()
        answer11=answer11.replace("\\","/")
        print("Dir changed to /"+answer11)
    flag=0
    

def pwd():
    print("Requesting path.....")
    try:
        s.send("PWD".encode())
    except:
        print ("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
       answer= s.recv(BUFFER_SIZE).decode()
       if(answer=="."):
           answer="/"
           print("\n\t"+answer)
       else:
           answer=answer.replace("\\","/")
           print("\n\t /"+answer)
           
           
        
       return
    except:
        print("We dont have access to the current directory.")
    
def conn():
    print ("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print ("Connection sucessful")
    except:
        print ("Connection unsucessful. Make sure the server is online.")



def list_files():
    
    print ("Requesting files...\n")
    try:
        s.send("LIST".encode())
    except:
        print ("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        number_of_files = struct.unpack("i", s.recv(4))[0]
        for i in range(int(number_of_files)):
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            file_size = struct.unpack("i", s.recv(4))[0]
            print ("\t{} - {}b".format(file_name, file_size))
            s.send("1".encode())
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print ("Total directory size: {}b".format(total_directory_size))
    except:
        print ("Couldn't retrieve listing")
        return
    try:
        s.send("1".encode())
        return
    except:
        print ("Couldn't get final server confirmation")
        return


def dwld(file_name):
    print ("Downloading file: {}".format(file_name))
    try:
        s.send("DWLD".encode())
    except:
        print ("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE).decode()
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print ("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print ("Error checking file")
    ##########################################################
    try:
        SP = s.recv(1024).decode()
        Fsocket = socket(AF_INET , SOCK_STREAM)
        Fsocket.connect(("127.0.0.1" , int(SP)))
        File = open(file_name , "wb")
        FileContent  = b""
        while True:
            Temp = Fsocket.recv(1024)
            if Temp:
                FileContent += Temp
            else:
                break
        Fsocket.close()
        File.write(FileContent)
        File.close()    
    except:
        print("nashod")
        return


    #####################################################
    try:
        s.send("1".encode())
        print ("Successfully downloaded {}".format(file_name))
        s.send("1".encode())
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print ("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
        print("Colsing data TCP connection")
        print("Ack sent to control TCP connection")
    except:
        print ("Error downloading file")
        return
    return



def quit():
    s.send("QUIT".encode())
    s.recv(BUFFER_SIZE).decode()
    s.close()
    print ("Server connection ended")
    return

help()
while True:
    prompt = input("\nEnter a command: ")
    if(prompt[:4].upper())=="HELP":
        help()
    elif(prompt[:3].upper())=="PWD":
        pwd()
    elif(prompt[:2].upper())=="CD":
        cd(prompt[3:])
    elif prompt[:4].upper() == "CONN":
        conn()
    elif prompt[:4].upper() == "LIST":
        list_files()
    elif prompt[:4].upper() == "DWLD":
        dwld(prompt[5:])
    elif prompt[:4].upper() == "QUIT":
        quit()
        break
    else:
        print ("Command not recognised; please try again")
