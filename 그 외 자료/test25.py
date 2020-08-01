
'''
[ import library list]

1. pyrealsense2
   d

2. pandas
   d

3. cv2
   d

4. os
   d

5. tkinter
   d

6. matplotlib
   d

7. FigureCanvasTkAgg
   d

8. mplot3d
   d

    
9. PIL
   d

'''
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
from datetime import datetime


'''
Realsense_mapping class

   1.  __init__()
      화면을 생성하고 버튼과 캔버스를 배치합니다.
       
   2. Mapping_start()
      start 버튼을 클릭하면 동작합니다.
      카메라가 이동한 좌표를 매핑하고, 이동하는 정면을 카메라로 출력하는 기능이 있습니다.
      매핑작업은 3d 그래프를 사용해서 그렸으며, 그려진 좌표들을 순서대로 데이터프레임에 저장합니다.
      
   3. Mapping_stop()
      stop 버튼을 클릭하면 동작합니다.
      전역 플래그 변수 count와 key를 사용해서 진행중인 작업을 중단합니다.      

   4. Map_save()
      save 버튼을 클릭하면 동작합니다.
      카메라가 이동한 좌표가 저장된 데이터 프레임을 엑셀파일에 저장합니다.

   5. Map_load()
      좌표가 저장된 엑셀파일을 읽어와서 카메라가 이동한 경로를 그립니다.

'''
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
            has_frame, frame = capture.read()

            if not has_frame:
                print('Cant get frame')
            
            cv2.imshow('frame', frame)
                      
            if key == 1:
                print('Mapping camera stop')                   
                capture.release()
                cv2.destroyAllWindows()      
                pipe.stop()
                break
            
            frames = pipe.wait_for_frames()
            pose = frames.get_pose_frame()

            if pose:
                data = pose.get_pose_data()
                position_count = position_count+1
                print("position_count: {}", data.translation)
                df.loc[position_count] = (data.translation.x, data.translation.y, data.translation.z)
                
            ax.scatter(df.x[position_count], df.y[position_count], df.z[position_count], s=10, c = 'b')
            loadMap = FigureCanvasTkAgg(fig, master=window)
            Map_widget = loadMap.get_tk_widget()
            Map_widget.place(x=455, y=105)
            window.update_idletasks()
            window.update()            
            
                
    def Mapping_stop(self):
        print("Press Mapping stop button")
        
    def Map_save(self):
        print("c")
        
    
    def Map_load(self):
        print("Mapload")


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

