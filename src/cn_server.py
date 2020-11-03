import socket
import sys
import operator
from thread import start_new_thread
from threading import Lock
from time import *
lock = Lock()
HOST = '' # all availabe interfaces
PORT = 9999 # arbitrary non privileged port 
ansers=dict()
tosend=dict()
tostore=dict()
recivedstuff=dict()
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    
    sys.exit(0)

print("[-] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    print("[-] Socket Bound to port " + str(PORT))
except : 
    
    sys.exit()

s.listen(10)
print("Listening...")

# The code below is what you're looking for ############

questions = []
file = open("questions.txt", "r")
line = file.readline()
j=1
while(line != ""):
    questionString = line+"$"
    answers = []
    for i in range (4):
        answers.append(file.readline()+"$")

    correctLetter = file.readline()
    correctLetter = correctLetter[:-1]+"$"
    
    tosend[j]= (questionString,answers,correctLetter)
    tostore[j]=(questionString,correctLetter)
    
    line = file.readline()
    j=j+1
file.close()


def client_thread(conn):
    
    
    username=conn.recv(1024).decode()

    print(username)
    for i in range(1,j) :
        value=tosend[i]
        
        tobesent=value[0]+value[1][0]+value[1][1]+value[1][2]+value[1][3]+value[2]
        #question and four options and correct answers
        conn.send(tobesent.encode())
        
        
    #conn.send("".decode())
    marks=conn.recv(1).decode()
    #print(marks)
    global recivedstuff
    lock.acquire()
    recivedstuff[username]=marks
    lock.release()
    print(sorted(recivedstuff.items(), key=operator.itemgetter(1)))
    conn.close()
    

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))


    start_new_thread(client_thread, (conn,))
   

s.close()
