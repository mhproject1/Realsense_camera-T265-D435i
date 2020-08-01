
import pyrealsense2 as rs
import pandas as pd
import cv2
import os
import tkinter as tk
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from tkinter import *



class Realsense_mapping:
    def __init__(self, window):
        self.window = window
        self.window.title("T265 Mapping")
        self.window.geometry("1280x800")
        self.window.resizable(False, False)
        
        self.t265start = tk.Button(window, overrelief="solid", text="start", font=15, width=10, height=3, command=self.Mapping_start, repeatdelay=1000)
        self.t265start.place(x=60, y=130)

        self.t265stop = tk.Button(window, overrelief="solid", text="stop", font=15, width=10, height=3, command=self.Mapping_stop, repeatdelay=1000)
        self.t265stop.place(x=235, y=130)

        self.mapsave = tk.Button(window, overrelief="solid", text="Mapsave", font=15, width=10, height=3, command=self.Map_save, repeatdelay=1000)
        self.mapsave.place(x=60, y=230)

        self.mapload = tk.Button(window, overrelief="solid", text="Mapload", font=15, width=10, height=3, command=self.Map_load, repeatdelay=1000)
        self.mapload.place(x=235, y=230)

        self.Show_Map=tk.Canvas(window, width=750, height = 600, relief="solid", bd=2)
        self.Show_Map.place(x=450, y=100)

        self.Show_Cam=tk.Canvas(window, width=350, height = 350, relief="solid", bd=2)
        self.Show_Cam.place(x=50, y=350)


    def Mapping_start(self):
        print("Press Mapping start button")
        global key
        key = 0
        position_count = 0

        capture = cv2.VideoCapture(1)

        fig = Figure(figsize=(7.5, 6))        
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(left = -5, right = 5)
        ax.set_ylim(bottom = -5, top = 5)
        ax.set_zlim(bottom = -5, top = 5)
        
        pipe.start(cfg)

        while True:

            if key == 1:
                print('Mapping camera stop')                   
                capture.release()
                cv2.destroyAllWindows()      
                pipe.stop()
                break            
            
            has_frame, frame = capture.read()

            if not has_frame:
                print('Cant get frame')
                
            cv2.imshow('D435i screen', frame)
            
            frames = pipe.wait_for_frames()
            pose = frames.get_pose_frame()

            if pose:
                data = pose.get_pose_data()
                position_count = position_count+1
                print("position_count: {}", data.translation)
                df.loc[position_count] = (data.translation.x, data.translation.y, data.translation.z)
                
            ax.scatter(df.x[position_count], df.y[position_count], df.z[position_count], s=5, c = 'b')
            loadMap = FigureCanvasTkAgg(fig, master=window)
            Map_widget = loadMap.get_tk_widget()
            Map_widget.place(x=455, y=105)
            time.sleep(0.1)
            window.update_idletasks()
            window.update()            
                

               
    def Mapping_stop(self):
        print("Press Mapping stop button")
        global count
        global key
        count = 1
        key = 1
        
    def Map_save(self):
        print("c")
        date = datetime.today().strftime("%Y-%m-%d %H_%M_%S") + ".xlsx"

        base_dir = "C:/Users/nerin/OneDrive/바탕 화면/python test/project"
        file_name = date
        xlxs_dir = os.path.join(base_dir, file_name)

        df.to_excel(xlxs_dir,
                    sheet_name = 'Mapping_position',
                    na_rep = 'NaN',
                    float_format = "%.15f",
                    header = True,
                    index = True,
                    index_label = "num",
                    startrow = 0,
                    startcol = 0)        

        print("ok")
        
    def Map_load(self):
        print("Mapload")
        global count
        count = 0

        Mapdata = filedialog.askopenfilename(initialdir = "/",
                                                             title = "choose Mapping data",
                                                             filetypes = (("excel files", "*.xlsx"), ("all files","*.*")))
                
        pd_Mapdata = pd.read_excel(Mapdata)

        fig = Figure(figsize=(7.5, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.set_xlim(left = -5, right = 5)
        ax.set_ylim(bottom = -5, top = 5)
        ax.set_zlim(bottom = -5, top = 5)

        for i in range(0, len(pd_Mapdata)):        
            ax.scatter(pd_Mapdata.x[i], pd_Mapdata.y[i], pd_Mapdata.z[i], s=5, c = 'b')          
            
            loadMap = FigureCanvasTkAgg(fig, master=window)
            Map_widget = loadMap.get_tk_widget()
            Map_widget.place(x=455, y=105)
            
            time.sleep(0.1)
            window.update_idletasks()
            window.update()
        
            if(count == 1):
                break


df = pd.DataFrame(columns=['x', 'y', 'z'])
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe = rs.pipeline()

window= Tk()

background = tk.PhotoImage(file = "./background2.gif")
bg_label = tk.Label(window, image=background)
bg_label.place(x=0, y=0)

start= Realsense_mapping(window)
window.mainloop()


