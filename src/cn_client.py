from tkinter import * 
import socket
answersselected=""
right=0
def closee():
	s.send(str(right).encode())
	s.close()
class Question:
    def __init__(self, question, answers,correctLetter):
        self.question = question
        self.answers = answers
        self.correctLetter = correctLetter

    def check(self, letter, view):
        global right
        if(letter == self.correctLetter):
            #label = Label(view, text="Right!")
            right += 1
        '''else:
            label = Label(view, text="Wrong!")
        #label.pack()'''
        view.after(1000, lambda *args: self.unpackView(view))
        #s.send(letter)
        return letter


    def getView(self, window):
        view = Frame(window)
        Label(view, text=self.question).pack()
        Button(view, text=self.answers[0], command=lambda *args: self.check("A", view)).pack()
        Button(view, text=self.answers[1], command=lambda *args: self.check("B", view)).pack()
        Button(view, text=self.answers[2], command=lambda *args: self.check("C", view)).pack()
        Button(view, text=self.answers[3], command=lambda *args: self.check("D", view)).pack()
        return view

    def unpackView(self, view):
        view.pack_forget()
        askQuestion()

def askQuestion():
    global questions, window, index, button, right, number_of_questions 
    if(len(questions) == index + 1):
        Label(window, text="Thank you for taking the test and your score is "+str(right) +" out of 4").pack()
        closee()
        #print(right)
        #s.send(str(right).encode())
        #s.close()
        #s.send(answersselected.encode())
        return
    button.pack_forget()
    index += 1
    questions[index].getView(window).pack()
    

def Main():
    #print("Send 'q' to exit\n")
    #address = input("ip:port -> ")
    #print("adres",address.index(":"))
    address='127.0.0.1:9999'
    username = input("username: ")
    

    try:
        if address.index(":") != 0:
            host = address[:address.index(":")]
            port = int(address[address.index(":")+1:])
    except ValueError:
        host = address
        port = 5000
    global s
    s = socket.socket()
    s.connect((host, port))
    s.send(username.encode())
    data='hehe'
    print("Welcome "+username)
    option=list()
    recieved=""
    while data!="":
        #print("here")
        option=list()
        data = s.recv(1024)
        #print(data)
        #print("empty")
        data = data.decode()
        #print(data)
        recieved=recieved+data
        if data=='' or data[-7:]=='$Me\n$A$' :
            break
    #print("1")   
    #print(recieved)  
    #print("fvb") 
    listt=recieved.split("$")
    #print(listt)
    lenn=len(listt)
    
    lenn=int((lenn-1)/6)
    #print(lenn)
    for i in range(lenn):
     option=list()
     i=i*6
     question=listt[i]
     option.append(listt[i+1])
     option.append(listt[i+2])
     option.append(listt[i+3])
     option.append(listt[i+4])
     correctanswer=listt[i+5]
     
     questions.append(Question(question, option,correctanswer))
    

questions = []
Main()
index = -1
right = 0
number_of_questions = len(questions)

window = Tk()
button = Button(window, text="Start", command=askQuestion)
button.pack()
window.mainloop()

#s.close()









