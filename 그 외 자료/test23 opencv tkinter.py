import numpy as np
import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")

#Graphics window
#imageFrame = tk.Frame(window, width=600, height=500)
#imageFrame.grid(row=0, column=0, padx=10, pady=2)
#Show_Cam=tk.Frame(window, width=300, height=300)
#Show_Cam.place(x=0, y=0)

#Capture video frames

cap = cv2.VideoCapture(1)

def show_frame():
       has_frame, frame = cap.read()

       if not has_frame:
              print("cant get frame")

       display1 = tk.Label(window, width=300, height=300)
       display1.place(x=0, y=0)
       
       cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
       img = Image.fromarray(cv2image)
       imgtk = ImageTk.PhotoImage(image=img)
       display1.imgtk = imgtk #Shows frame for display 1
       display1.configure(image=imgtk)
       window.after(10, show_frame) 

show_frame() #Display
window.mainloop()  #Starts GUI


