import tkinter as tk
from certifi import contents
from numpy import char
import speech_recognition as sr
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(host="localhost",user="root",database="transcribe",passwd="123456")


while True:
    user=input("enter your name : ")
    break

root = tk.Tk()
root.title("audio to text converter")
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)


#instructions
instructions = tk.Label(root, text="Select a audio file", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)


def open_file():
    browse_text.set("loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("audio file", "*.wav")])
    if file:
        sound = (file)
        r = sr.Recognizer()
        with sr.AudioFile(sound) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            
            report = open('output.txt','w')
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            report.write (text)
            report.close()

            time_now = datetime.now()
            dStr = time_now.strftime("%y-%m-%d")
            tStr = time_now.strftime("%H:%M:%S")
            
            mycursor= mydb.cursor()
            s="INSERT INTO books (Date,USER,Transcribe_Data,Time) VALUES(%s,%s,%s,%s) "
            b1=(dStr,user,text,tStr)
            mycursor.execute(s,b1)
            mydb.commit()

            page =open('output.txt','r')
            content=page.read()
            print(content)
            print(user)

            

            text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
            text_box.insert(tk.END,content)
            text_box.tag_configure("center", justify="center")
            text_box.tag_add("center", 1.0, "end")
            text_box.grid(column=1, row=3)

            page.close()
            print("thanks")
            
    browse_text.set("Browse")

#browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=1, row=2)

canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3)

root.mainloop()
