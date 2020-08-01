import matplotlib
matplotlib.use("TkAgg") # set the backend
import matplotlib.pyplot as plt

plt.figure()
plt.plot([0,1,2,0,1,2]) # draw something
plt.show(block=False)

plt.get_current_fig_manager().window.wm_geometry("+600+800") # move the window
