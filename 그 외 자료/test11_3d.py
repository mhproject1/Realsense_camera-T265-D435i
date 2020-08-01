# plotting random walk by normal dist. 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np 

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d') # Axe3D object
ax.set_xlim(xmin = -5, xmax = 5)
ax.set_ylim(ymin = -5, ymax = 5)
ax.set_zlim(zmin = -5, zmax = 5)

x = 0.208036
y = 0.379415
z = 0.237536
ax.scatter(x, y, z, s=10, c = 'b')
plt.title("ax")
plt.show()

'''
# scattering 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np 

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d') # Axe3D object

sample_size = 500
x = np.cumsum(np.random.normal(0, 5, sample_size))
y = np.cumsum(np.random.normal(0, 5, sample_size))
z = np.cumsum(np.random.normal(0, 5, sample_size))
ax.scatter(x, y, z, c = z, s= 20, alpha=0.5, cmap=plt.cm.Greens)
plt.savefig('../../assets/images/markdown_img/180612_1225_3dplotting_scattering.svg')
plt.title("ax.scatter")
plt.show()

# contour3d
x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection='3d')
ax.contour3D(x, y, z, 20, cmap=plt.cm.rainbow)
#ax.view_init(45, 45) 방향 돌려서 보기. 
plt.savefig('../../assets/images/markdown_img/180612_1225_3dplotting_contour.svg')
plt.title("ax.contour3D")
plt.show()
'''



