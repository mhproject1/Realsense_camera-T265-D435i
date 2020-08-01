import pyrealsense2 as rs
import pandas as pd
import numpy as np
import time
import os
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
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

        fig = Figure(figsize=(7.5, 6))
        ax = fig.add_subplot(111)
        ax.set_xlim(xmin = -5, xmax = 5)
        ax.set_ylim(ymin = -5, ymax = 5)
                                
        i = 0        
        pipe.start(cfg)

        while True:
            frames = pipe.wait_for_frames()
            pose = frames.get_pose_frame()

            if pose:
                data = pose.get_pose_data()
                i = i+1
                #print("i : ", i, "\tx :", data.translation.x, "\ty : ", data.translation.y, data.translation.z)
                print("i : {}", data.translation)
                df.loc[i] = (data.translation.x, data.translation.y)
                
            ax.scatter(df.x[i], df.y[i], s=10, c = 'b')
            loadMap = FigureCanvasTkAgg(fig, master=window)
            Map_widget = loadMap.get_tk_widget()
            Map_widget.place(x=455, y=105)
            window.update_idletasks()
            window.update()            
            
                
    def stop(self):
        print("b")
        global count
        count = 1
        pipe.stop()

    def save(self):
        print("c")
        df.to_excel(xlxs_dir,
                    sheet_name = 'T265_position',
                    na_rep = 'NaN',
                    float_format = "%.15f",
                    header = True,
                    index = True,
                    index_label = "num",
                    startrow = 0,
                    startcol = 0)        

        print("ok")
    
    def load(self):
        print("Mapload")
        global count
        count = 0
        read_df = pd.read_excel(xlxs_dir, sheet_name='T265_position', usecols=[1,2])

        fig = Figure(figsize=(7.5, 6))
        ax = fig.add_subplot(111)
        ax.set_xlim(xmin = -5, xmax = 5)
        ax.set_ylim(ymin = -5, ymax = 5)       
        
        for i in range(0, len(read_df)):
            ax.scatter(read_df.x[i], read_df.y[i], s=10, c = 'b') 

            window.update_idletasks()
            window.update()
            loadMap = FigureCanvasTkAgg(fig, master=window)
            Map_widget = loadMap.get_tk_widget()
            Map_widget.place(x=455, y=105)

            if(count == 1):
                break


# base_dir에서 excel 파일이 저장될 경로를 설정해야 함
base_dir = "C:/Users/nerin/OneDrive/바탕 화면/python test/project"
file_name = "df.xlsx"
xlxs_dir = os.path.join(base_dir, file_name)

df = pd.DataFrame(columns=['x', 'y'])

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe = rs.pipeline()

window= Tk()

background = tk.PhotoImage(file = "./background2.gif")
bg_label = tk.Label(window, image=background)
bg_label.place(x=0, y=0)

start= t265_mapping(window)
window.mainloop()

