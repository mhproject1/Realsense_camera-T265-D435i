
# T&D Mapping program

'''
**********************************************************************************************************

[ import library list]

1. pyrealsense2   
    intel realsense sdk 2.0은 intel realsense camera용 크로스 플랫폼 라이브러리로,
    Intel realsense viewer 프로그램을 설치하면 해당 realsense camera의 기능을 사용할 수 있습니다.

    이것을 우리가 프로그래밍 언어로 직접 접근하기 위해 librealsense라는 라이브러리를 사용합니다.
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
import numpy as np 
import cv2
import os
import tkinter as tk
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from tkinter import *
from matplotlib import pyplot as plt


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

   6. Exit()
      모든 창을 종료합니다
      
**********************************************************************************************************
'''

class Realsense_mapping:
            
    def __init__(self, window):
        self.window = window
        self.window.title("T&D Mapping program")
        self.window.geometry("900x561+100+100")
        self.window.resizable(False, False)

        self.Start = PhotoImage(file = "./start.gif")
        self.Stop = PhotoImage(file = "./stop.gif")
        self.Save = PhotoImage(file = "./mapsave.gif")
        self.Load= PhotoImage(file = "./mapload.gif")
        self.Exit = PhotoImage(file = "./exit.gif")        
        
        self.t265start = tk.Button(window, overrelief="solid", image = self.Start, width=150, height=40, command=self.Mapping_start, repeatdelay=1000)
        self.t265start.place(x=700, y=200)

        self.t265stop = tk.Button(window, overrelief="solid", image = self.Stop, width=150, height=40, command=self.Mapping_stop, repeatdelay=1000)
        self.t265stop.place(x=700, y=270)

        self.mapsave = tk.Button(window, overrelief="solid", image = self.Save,width=150, height=40, command=self.Map_save, repeatdelay=1000)
        self.mapsave.place(x=700, y=340)

        self.mapload = tk.Button(window, overrelief="solid", image = self.Load, width=150, height=40, command=self.Map_load, repeatdelay=1000)
        self.mapload.place(x=700, y=410)

        self.closeWindow = tk.Button(window, overrelief="solid", image = self.Exit, width=150, height=40, command=self.exit, repeatdelay=1000)
        self.closeWindow.place(x=700, y=480)


    def Mapping_start(self):
        print("Press Mapping start button")
        global key
        key = 0
        position_count = 0

        profile = pipeline.start(config)
        pipe.start(cfg)

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)

        clipping_distance_in_meters = 1 
        clipping_distance = clipping_distance_in_meters / depth_scale

        align_to = rs.stream.color
        align = rs.align(align_to)

        map = plt.figure()
        map_ax = Axes3D(map)
        map_ax.autoscale(enable=True, axis='both', tight=True)
        
        map_ax.set_xlim3d([-1.0, 1.0])
        map_ax.set_ylim3d([-1.0, 1.0])
        map_ax.set_zlim3d([-1.0, 1.0])
        mh_Mapping, = map_ax.plot3D([0], [0], [0])

        while True:
            
            if key == 1:
                print('Mapping camera stop')
                plt.close()
                cv2.destroyAllWindows()      
                pipe.stop()
                pipeline.stop()
                break

            tframe = pipe.wait_for_frames()
            dframe = pipeline.wait_for_frames()
                        
            aligned_frames = align.process(dframe)

            aligned_depth_frame = aligned_frames.get_depth_frame() 
            color_frame = aligned_frames.get_color_frame()

            if not aligned_depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            grey_color = 153
            depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) 
            bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            images = np.hstack((color_image, bg_removed, depth_colormap))
            cv2.namedWindow('T&D Mapping Camera', cv2.WINDOW_AUTOSIZE)            
            cv2.imshow('T&D Mapping Camera', images)
            cv2.moveWindow('T&D Mapping Camera', 100, 700)
            key = cv2.waitKey(1)

            pose = tframe.get_pose_frame()

            if pose:
                data = pose.get_pose_data()
                position_count = position_count+1
                print("position_count: {}", data.translation)
                df.loc[position_count] = (data.translation.x, data.translation.y, data.translation.z)

                xdata, ydata, zdata = mh_Mapping._verts3d
                mh_Mapping.set_xdata(list(np.append(xdata, data.translation.x)))
                mh_Mapping.set_ydata(list(np.append(ydata, data.translation.y)))
                mh_Mapping.set_3d_properties(list(np.append(zdata, data.translation.z)))
                
                plt.draw()
                plt.get_current_fig_manager().window.wm_geometry("+1030+100")
                plt.pause(0.01)
                
                
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

        print("save success")

        
    
    def Map_load(self):        
        print("Mapload")
        global count
        count = 0

        Mapdata = filedialog.askopenfilename(initialdir = "/",
                                                             title = "choose Mapping data",
                                                             filetypes = (("excel files", "*.xlsx"), ("all files","*.*")))
                
        pd_Mapdata = pd.read_excel(Mapdata)

        map = plt.figure()
        map_ax = Axes3D(map)
        map_ax.autoscale(enable=True, axis='both', tight=True)

        map_ax.set_xlim3d([-1.0, 1.0])
        map_ax.set_ylim3d([-1.0, 1.0])
        map_ax.set_zlim3d([-1.0, 1.0])
        mh_Mapping, = map_ax.plot3D([0], [0], [0])

        for i in range(0, len(pd_Mapdata)):
            print("position_count: {} x:", pd_Mapdata.x[i], " y:", pd_Mapdata.y[i], " z:", pd_Mapdata.z[i])
            xdata, ydata, zdata = mh_Mapping._verts3d            
            mh_Mapping.set_xdata(list(np.append(xdata, pd_Mapdata.x[i])))
            mh_Mapping.set_ydata(list(np.append(ydata, pd_Mapdata.y[i])))
            mh_Mapping.set_3d_properties(list(np.append(zdata, pd_Mapdata.z[i])))
            plt.draw()
            plt.get_current_fig_manager().window.wm_geometry("+1100+100")
            plt.pause(0.01)

            if(count == 1):
                plt.close()
                break

        print("load success")

        

    def exit(self):
        print("exit")
        self.window.destroy()
        

df = pd.DataFrame(columns=['x', 'y', 'z'])

pipeline = rs.pipeline()
pipe = rs.pipeline()

config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

window= Tk()

background = tk.PhotoImage(file = "./bg.gif")
bg_label = tk.Label(window, image=background)
bg_label.place(x=0, y=0)

start= Realsense_mapping(window)
window.mainloop()

