from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import pyttsx3
import speech_recognition
import threading

bot=ChatBot('Bot')
trainer=ListTrainer(bot)
for files in os.listdir('data/english/'):

    data=open('data/english/'+files,'r',encoding='utf-8').readlines()


    trainer.train(data)

def botReply():
    question=questionField.get()
    question=question.capitalize()
    answer=bot.get_response(question)
    textarea.insert(END,'You: '+question+'\n\n')
    textarea.insert(END, 'Zax: ' + str(answer)+'\n\n')
    pyttsx3.speak(answer)
    questionField.delete(0,END)



def audioToText():
    while True:
        sr=speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone()as m:
                sr.adjust_for_ambient_noise(m,duration=0.2)
                audio=sr.listen(m)
                query=sr.recognize_google(audio)



                questionField.delete(0,END)
                questionField.insert(0,query)
                botReply()

        except Exception as e:
            print(e)

def voiceChange():
    eng = pyttsx3.init()
    voice = eng.getProperty('voices')

    eng.setProperty('voice', voice[1].id)
    eng.say("Welcome . This is our Bot Zax ! Zax is here to help you ! Stay put.")
    eng.runAndWait()


if __name__ == "__main__":
    voiceChange()



root=Tk()

root.geometry('500x570+100+30')

root.title('Meet with Zax!!')
root.config(bg='grey24')

logoPic=PhotoImage(file='pic__1.png')

logoPicLabel= Label(root,image=logoPic, bg='grey24')

logoPicLabel.pack(pady=5)

centerFrame=Frame(root)
centerFrame.pack()

scrollbar=Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)

textarea=Text(centerFrame,font=('times new roman',17,'bold'),height=10,yscrollcommand=scrollbar.set,wrap='word')
textarea.pack(side=LEFT)
scrollbar.config(command=textarea.yview())

questionField = Entry(root,font=('times new roman',15,'bold'))
questionField.pack(pady=15,fill=X)


askPic=PhotoImage(file='ask.png')
askButton=Button(root,image=askPic,command=botReply)
askButton.pack()


def click(event):
    askButton.invoke()

root.bind('<Return>',click)

thread=threading.Thread(target=audioToText)
thread.setDaemon(True)
thread.start()

root.mainloop()