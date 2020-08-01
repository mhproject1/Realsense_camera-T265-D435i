import pyrealsense2 as rs
import pandas as pd
import numpy as np
import time
import cv2
import os
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from tkinter import *
from PIL import Image
from PIL import ImageTk

class t265_mapping:
    def __init__(self, window):
        self.window = window
        self.window.title("T265 Mapping")
        self.window.geometry("1280x800")
        self.window.resizable(False, False)

        self.t265start = tk.Button(window, overrelief="solid", text="start", font=15, width=10, height=3, command=self.start, repeatdelay=1000)
        self.t265start.place(x=60, y=130)

        self.t265stop = tk.Button(window, overrelief="solid", text="stop", font=15, width=10, height=3, command=self.stop, repeatdelay=1000)
        self.t265stop.place(x=235, y=130)

        self.mapsave = tk.Button(window, overrelief="solid", text="Mapsave", font=15, width=10, height=3, command=self.save, repeatdelay=1000)
        self.mapsave.place(x=60, y=230)

        self.mapload = tk.Button(window, overrelief="solid", text="Mapload", font=15, width=10, height=3, command=self.load, repeatdelay=1000)
        self.mapload.place(x=235, y=230)

        self.Show_Map=tk.Canvas(window, width=750, height = 600, relief="solid", bd=2)
        self.Show_Map.place(x=450, y=100)

        #self.Show_Cam=tk.Canvas(window, width=350, height = 350, relief="solid", bd=2)
        #self.Show_Cam=tk.Frame(window, width=350, height = 350)
        #self.Show_Cam.place(x=50, y=350)        
      
    def start(self):
        print("a")
        global key
        key = 0

        cap = cv2.VideoCapture(1)
        display1 = tk.Label(window, width=350, height = 350)
        display1.place(x=50, y=350)

        def show_frame():
            has_frame, frame = cap.read()
            if not has_frame:
                print("cant get frame")
                
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            display1.imgtk = imgtk
            display1.configure(image=imgtk)
            window.after(10, show_frame)        
                    

        while True:          
            show_frame() #Display

        
        '''
        cap = cv2.VideoCapture(1)

        def show_frame():
               has_frame, frame = cap.read()

               if not has_frame:
                      print("cant get frame")

               display1 = tk.Label(window, width=350, height = 350)
               display1.place(x=50, y=350)   
               
               cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
               img = Image.fromarray(cv2image)
               imgtk = ImageTk.PhotoImage(image=img)
               display1.imgtk = imgtk #Shows frame for display 1
               display1.configure(image=imgtk)
               window.after(10, show_frame) 

        show_frame() #Display
        #window.update_idletasks()
        #window.update()     
        '''
        
    def stop(self):
        print("b")
        global key
        key = 1

    def save(self):
        print("c")

        
    def load(self):
        print("Mapload")


window= Tk()

background = tk.PhotoImage(file = "./background2.gif")
bg_label = tk.Label(window, image=background)
bg_label.place(x=0, y=0)

start= t265_mapping(window)
window.mainloop()

