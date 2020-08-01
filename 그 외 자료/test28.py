import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

import time

import tkinter as tk
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
from datetime import datetime
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
def update_Mapping(hl, new_data):
	xdata, ydata, zdata = hl._verts3d
	hl.set_xdata(list(np.append(xdata, new_data[0])))
	hl.set_ydata(list(np.append(ydata, new_data[1])))
	hl.set_3d_properties(list(np.append(zdata, new_data[2])))
	plt.draw()
 
 
map = plt.figure()
map_ax = Axes3D(map)
map_ax.autoscale(enable=True, axis='both', tight=True)
 
# # # Setting the axes properties
map_ax.set_xlim3d([-5.0, 5.0])
map_ax.set_ylim3d([-5.0, 5.0])
map_ax.set_zlim3d([-5.0, 5.0])
 
hl, = map_ax.plot3D([0], [0], [0])

Mapdata = filedialog.askopenfilename(initialdir = "/",
                                     title = "choose Mapping data",
                                     filetypes = (("excel files", "*.xlsx"), ("all files","*.*")))

pd_Mapdata = pd.read_excel(Mapdata)


for i in range(0, len(pd_Mapdata)):
    x = pd_Mapdata.x[i]
    y = pd_Mapdata.y[i]
    z = pd_Mapdata.z[i]
    
    update_Mapping(hl, (x, y, z))
    plt.show(block=False)
    plt.pause(0.01)
    print(i)

'''

class Realsense_mapping:
            
    def __init__(self, window):
        self.window = window
        self.window.title("T&D Mapping program")
        self.window.geometry("950x480")
        self.window.resizable(False, False)

        self.text=tk.Text(window)
        self.text.pack()

    def test(self):
        
        for i in range(0, 10):
            text.insert(2.1, i)
            time.sleep(0.5)
            self.text.delete(1)
       
window= Tk()
start= Realsense_mapping(window)
window.mainloop()















