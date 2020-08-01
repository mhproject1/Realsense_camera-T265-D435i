import pandas as pd
import os
import tkinter as tk
import matplotlib.pyplot as plt
import pyrealsense2 as rs
import time
from tkinter import *

# base_dir에서 excel 파일이 저장될 경로를 설정해야 함
base_dir = "C:/Users/nerin/OneDrive/바탕 화면/python test/project"
file_name = "df.xlsx"
xlxs_dir = os.path.join(base_dir, file_name)

# 파일을 남겨두고 싶으면 df이름을 바꿔줘야 함
# df1, df2, df3, ...
df = pd.DataFrame(columns=['x', 'y'])

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe = rs.pipeline()

def start():
    i = 0
    pipe.start(cfg)    

    while True:          
        frames = pipe.wait_for_frames()
        pose = frames.get_pose_frame()

        if pose:
            data = pose.get_pose_data()           
            i = i+1
            print("i : ", i, "\tx :", data.translation.x, "\ty : ", data.translation.y)
            df.loc[i] = (data.translation.x, data.translation.y)

        window.update_idletasks()
        window.update()
        time.sleep(0.1)
    
def stop():
    global count
    pipe.stop()

def save():
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
    

def load():
    print("d")
    read_df = pd.read_excel(xlxs_dir, sheet_name='T265_position', usecols=[1,2])
    print(read_df.loc[1])

window=tk.Tk()
window.title("T265 Mapping")
window.geometry("1280x800")
window.resizable(False, False)

background = tk.PhotoImage(file = "./background2.gif")
bg_label = tk.Label(window, image=background)
bg_label.place(x=0, y=0)

t265start = tk.Button(window, overrelief="solid", text="start", font=15, width=10, height=3, command=start, repeatdelay=1000)
t265start.place(x=60, y=130)

t265stop = tk.Button(window, overrelief="solid", text="stop", font=15, width=10, height=3, command=stop, repeatdelay=1000)
t265stop.place(x=235, y=130)

mapsave = tk.Button(window, overrelief="solid", text="Mapsave", font=15, width=10, height=3, command=save, repeatdelay=1000)
mapsave.place(x=60, y=230)

mapload = tk.Button(window, overrelief="solid", text="Mapload", font=15, width=10, height=3, command=load, repeatdelay=1000)
mapload.place(x=235, y=230)

Show_Map=tk.Canvas(window, width=750, height = 600, relief="solid", bd=2)
Show_Map.place(x=450, y=100)

Show_Cam=tk.Canvas(window, width=350, height = 350, relief="solid", bd=2)
Show_Cam.place(x=50, y=350)

window.mainloop()













