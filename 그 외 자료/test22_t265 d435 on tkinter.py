
# T&D Mapping program

'''
**********************************************************************************************************

[ import library list]

1. pyrealsense2   
    intel realsense sdk 2.0은 intel realsense camera용 크로스 플랫폼 라이브러리로,
    Intel realsense viewer 프로그램을 설치하면 해당 realsense camera의 기능을 사용할 수 있습니다.

    이것을 우리가 프로그래밍 언어로 직접 접근하기 위해 librealsense라는 라이브러리리를 사용합니다.
    해당 라이브러리는 c++로 개발되어 있으며, 파이썬에서 librealsense api를 사용하기 위해서는
    pyrealsense2를 설치해야 합니다.

        - pip install pyrealsense2
        
2. pandas
   해당 프로그램에서는 카메라의 좌표를 처리하기 위해 dataframe을 사용합니다.

3. cv2
    opencv는 오픈소스 컴퓨터 비전 라이브러리로, 객체의 얼굴이나 행동 등을 인식할 수 있습니다.
    해당 프로그램에서는 librealsense 크로스 플랫폼 라이브러리에서 제공하는 api를 사용하지 않고
    opencv 라이브러리를 사용해서 Intel realsense D435i camera를 사용해서 화면을 출력합니다.

4. os
    파이썬에서 기본적으로 제공되는 모듈로 파일 복사, 디렉터리 생성 등 다양한 기능이 있는데,
    해당 프로그램에서는 특정 디렉터리 위치를 읽어오기 위해 사용합니다.

5. tkinter
    tkinter는 파이썬에서 GUI 프로그래밍을 할 때 사용하는 표준 인터페이스로,
    해당 프로그램에서는 새롭게 생성한 window창에 캔버스, 버튼 등을 사용해서 인터페이스를
    구성하는데 사용했습니다.

6. matplotlib
   matplotlib는 파이썬에서 데이터를 차트나 플롯으로 그려주는 라이브러리로,
   해당 프로그램에서는 카메라의 위치정보를 기반으로 3d 그래프를 그렸습니다.

      - matplotlib.use('TkAgg')      
      - from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib을 사용해서 그린 그래프를 tkinter의 캔버스에 출력하기 위한 백앤드 설정 및 라이브러리를
        추가로 임포트 했습니다.

        - from mpl_toolkits.mplot3d import Axes3D      
        해당 라이브러리는 명시적으로 사용하지는 않지만  3d 그래프를 그리기 위해 추가로 임포트 했습니다.
        
**********************************************************************************************************
'''

import pyrealsense2 as rs
import pandas as pd
import cv2
import os
import tkinter as tk
import matplotlib as plt
plt.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from tkinter import *

import gc

'''
**********************************************************************************************************

[Realsense_mapping class]

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
      
**********************************************************************************************************
'''

class Realsense_mapping:
    
    def __init__(self, window):
        self.window = window
        self.window.title("T&D Mapping program")
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
                window.update_idletasks()
                window.update()

        del position_count
        gc.collect()
                
                
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
            ax.scatter(pd_Mapdata.x[i], pd_Mapdata.y[i], pd_Mapdata.z[i], s=10, c = 'b') 

            window.update_idletasks()
            window.update()
            loadMap = FigureCanvasTkAgg(fig, master=window)
            Map_widget = loadMap.get_tk_widget()
            Map_widget.place(x=455, y=105)

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

