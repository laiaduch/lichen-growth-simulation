import numpy as np
import cv2
import matplotlib.pyplot as plt

def compute_sun_direction(sun_angle, camera_direction):
    # Define the direction of the sun (assuming the sun is at a specific angle from the north)
    sun_direction_north = np.array([np.sin(np.radians(sun_angle)), 0, np.cos(np.radians(sun_angle))])

    # Rotate the sun direction according to the camera direction
    if camera_direction == 'north':
        sun_direction = sun_direction_north
    elif camera_direction == 'south':
        sun_direction = -sun_direction_north
    elif camera_direction == 'west':
        sun_direction = np.array([0, np.sin(np.radians(sun_angle)), np.cos(np.radians(sun_angle))])
    elif camera_direction == 'east':
        sun_direction = np.array([0, -np.sin(np.radians(sun_angle)), -np.cos(np.radians(sun_angle))])
    else:
        raise ValueError("Invalid camera direction. Choose from 'north', 'south', 'east', or 'west'.")

    return sun_direction

# Load the input image of normals (assume that the image has 3 channels)
input_file = 'teulada1_normal.png'
normal_img = cv2.imread(f'./images/input_normal/{input_file}')

# Normalize the image between [-1,1]
normal_img = (normal_img / 255.0) * 2 - 1

# Define parameters
sun_angle = 70  # in degrees
camera_direction = 'east'  # User can choose from 'north', 'south', 'east', or 'west'

# Compute the direction of the sun based on user choice
sun_direction = compute_sun_direction(sun_angle, camera_direction)

# Compute the dot product
dot_product = np.sum(normal_img * sun_direction, axis=2)

# Define a threshold to consider the region as "highlighted"
highlight_threshold = 0

# Create a mask for highlighted areas
highlight_img = np.maximum(0, dot_product)

# Show results
plt.subplot(1, 2, 1)
plt.title("Normals")
plt.imshow(normal_img.astype(np.float32), cmap='gray')

plt.subplot(1, 2, 2)
plt.title("Areas Affected by Light")
plt.imshow(highlight_img.astype(np.float32), cmap='gray')
plt.show()

# Save the output image
output_path = './images/output_light'
output_file = f'{output_path}/{input_file}_light_{camera_direction}.png'
plt.imsave(output_file, highlight_img, cmap='gray')
