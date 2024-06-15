import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Load the input image of normals (assume that the image has 3 channels)
input_file = 'cortezaarbre_normal.png'
normal_img = Image.open(f'./images/input_normal/{input_file}')
normal_img = normal_img.convert('RGB')
normal_img = np.array(normal_img)

# Normalize the image between [-1,1]
normal_img = (normal_img / 255.0) * 2 - 1

# Rain direction (the vertical is (0, 0, 1))
vertical = np.array([0, -1, 0])

# Compute the dot product
dot_product = np.sum(normal_img * vertical, axis=2)

# Define a threshold to consider the region is affected by the rain
rain_threshold = 0

# Create a mask
highlight_img = np.maximum(dot_product, 0)

# Show results
plt.title("Areas Affected by Rain")
plt.imshow(highlight_img.astype(np.float32), cmap='gray')
plt.show()

# Save the output image
output_path = './images/output_rain'
output_file = f'{output_path}/{input_file}_rain.png'
plt.imsave(output_file, highlight_img, cmap='gray')

