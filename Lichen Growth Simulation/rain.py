import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load the input image of normals (assume that the image has 3 channels)
input_file = 'teulada2_normal.png'
normal_img = cv2.imread(f'./images/input_normal/{input_file}')

# Normalize the image between [-1,1]
normal_img = (normal_img / 255.0) * 2 - 1

# Rain direction (the vertical is (0, 0, 1))
vertical = np.array([0, -1, 0])

# Compute the dot product
dot_product = np.sum(normal_img * vertical, axis=2)

# Define a threshold to consider the region is affected by the rain
rain_threshold = 0

# Create a mask
#rain_mask = dot_product > rain_threshold
highlight_img = np.maximum(dot_product, 0)

# Create new image to show the affected regions
#highlight_img = np.zeros_like(normal_img)  # Black image
#highlight_img[rain_mask, :] = [255, 255, 255]  # Paint with white the affected regions

# Show results
plt.subplot(1, 2, 1)
plt.title("Normals")
plt.imshow(normal_img.astype(np.float32), cmap='gray')

plt.subplot(1, 2, 2)
plt.title("Areas Affected by Rain")
plt.imshow(highlight_img.astype(np.uint8))
plt.show()

# Save the output image
#highlight_img = np.clip(highlight_img, 0, 1) # Normalize the image between [0,1]
output_path = './images/output_rain'
output_file = f'{output_path}/{input_file}_rain.png'
plt.imsave(output_file, highlight_img, cmap='gray')

