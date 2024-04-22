import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load input image
input_file = 'rocks_normal.png'
normal_img = Image.open(f'./images/input_normal/{input_file}')

# Conver the image into a numpy array
normal_array = np.array(normal_img)

# Verify that the image has the correct format (3 channels for xyz)
assert normal_array.shape[-1] == 3, "The normal image must have 3 channels for x, y, z"

# Defines the direction of the rain (downwards). In this case, it would be (0, 0, 1)
rain_direction = np.array([0, 0, 1])

# Compute the dot product between the normals and rain direction
# dot_products = np.einsum('ijk,k->ij', normal_array, rain_direction)
dot_products_temp = normal_array * rain_direction  # Multiply each component by the direction vector
dot_products = np.sum(dot_products_temp, axis=2)  # The dot product is obtained by summing along the component axis

# Create a mask when the dot product is positive
rain_mask = dot_products > 0

# Create the output image where an output image where the points affected by the rain are white and the others are black
rain_effect_img = np.zeros_like(dot_products)
rain_effect_img[rain_mask] = 255  # The places affected by the rain are white

# Save the output image
output_path = './images/output_rain'
output_file = f'{output_path}/{input_file}_rain.png'
plt.imsave(output_file, rain_effect_img, cmap='gray')
