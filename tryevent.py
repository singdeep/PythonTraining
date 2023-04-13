#Import the Tkinter library
from tkinter import *
#Create an instance of Tkinter frame
win= Tk()
#Define the geometry
win.geometry("750x250")
#Define Event handlers with arguments
def event_show(event):
   button.config(bg="red", fg= "white")
   label.config(text="Hello World")
#Create a Label
label= Label(win, text="",font=('Helvetica 15 underline'))
label.pack()
#Create a frame
frame= Frame(win)
#Create Buttons in the frame
button= Button(frame, text="Click",command=lambda:event_show(button))
button.pack(pady=10)
frame.pack()
#Bind the function
win.bind('<Return>',lambda event:event_show(event))
win.mainloop()