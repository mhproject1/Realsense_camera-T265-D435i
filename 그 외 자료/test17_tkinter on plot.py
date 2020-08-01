import pandas as pd
import os
import tkinter as tk
import matplotlib.pyplot as plt
import pyrealsense2 as rs
import time
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

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

        self.Show_Cam=tk.Canvas(window, width=350, height = 350, relief="solid", bd=2)
        self.Show_Cam.place(x=50, y=350)


    def start(self):
        print("a")
        
    def stop(self):
        print("b")

    def save(self):
        print("c")
    
    def load(self):
        print("d")


window= Tk()

background = tk.PhotoImage(file = "./background2.gif")
bg_label = tk.Label(window, image=background)
bg_label.place(x=0, y=0)

start= t265_mapping(window)
window.mainloop()
