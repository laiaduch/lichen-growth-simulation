import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Definim la mida de la imatge
width, height = 512, 512

# Creem una graella de coordenades x i y
x = np.linspace(-1, 1, width)
y = np.linspace(-1, 1, height)
x, y = np.meshgrid(x, y)

# Calculem el radi per a cada punt (x, y)
z_squared = 1 - x**2 - y**2

# Inicialitzem les components de la normal
nx = np.zeros_like(x)
ny = np.zeros_like(y)
nz = np.zeros_like(z_squared)

# Els punts dins l'esfera tindran normals definides
mask = z_squared >= 0
z = np.sqrt(z_squared[mask])
nx[mask] = x[mask]
ny[mask] = y[mask]
nz[mask] = z

# Normalitzem les normals
normals = np.stack((nx, ny, nz), axis=-1)
normals /= np.linalg.norm(normals, axis=-1, keepdims=True)

# Convertim les normals a una imatge (amb valors entre 0 i 1)
normals_image = (normals + 1) / 2

# Ens quedem només amb la part de l'esfera
normals_image[~mask] = 0.5

# Guardem la imatge
plt.imsave('sphere_normals.png', normals_image)

# Mostrem la imatge per assegurar-nos que s'ha creat correctament
plt.imshow(normals_image)
plt.axis('off')
plt.show()
