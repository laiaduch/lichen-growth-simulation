import numpy as np
import cv2
import matplotlib.pyplot as plt

'''def compute_sun_direction(sun_angle, camera_direction):

    # Rotate the sun direction according to the camera direction
    if camera_direction == 'north':
        sun_direction = np.array([0, -np.sin(sun_angle),np.cos(sun_angle)])
    elif camera_direction == 'south':
        sun_direction = np.array([0, -np.sin(sun_angle), -np.cos(sun_angle)])
    elif camera_direction == 'east':
        sun_direction = np.array([-np.cos(sun_angle), -np.sin(sun_angle), 0])
    elif camera_direction == 'west':
        sun_direction = np.array([np.cos(sun_angle), -np.sin(sun_angle), 0])
    else:
        raise ValueError("Invalid camera direction. Choose from 'north', 'south', 'east', or 'west'.")

    # (-cos(70)*sin(a), -sin(70), -cos(70)*cos(a))
    # sun_direction = np.array([- np.cos(sun_angle) * np.sin(angle), -np.sin(sun_angle), -np.cos(sun_angle) * np.cos(angle)])

    return sun_direction'''

def compute_sun_direction(sun_angle, camera_direction):

    # Rotate the sun direction according to the camera direction
    if camera_direction == 'W':
        angle = - (np.pi / 2)
    elif camera_direction == 'S':
        angle = 0
    elif camera_direction == 'E':
        angle = np.pi / 2
    elif camera_direction == 'N':
        angle = np.pi
    else:
        raise ValueError("Invalid camera direction. Choose from 'N', 'S', 'E', or 'W'.")

    # (-cos(70)*sin(a), -sin(70), -cos(70)*cos(a))
    sun_direction = np.array([- np.cos(sun_angle) * np.sin(angle), -np.sin(sun_angle), -np.cos(sun_angle) * np.cos(angle)])

    return sun_direction

# Load the input image of normals (assume that the image has 3 channels)
input_file = 'teulada1_normal.png'
normal_img = cv2.imread(f'./images/input_normal/{input_file}')
#normal_img = cv2.imread('images/sphere_normals.png')

# Normalize the image between [-1,1]
normal_img = (normal_img / 255.0) * 2 - 1

# Define parameters
sun_angle = np.deg2rad(70)  # in rad
camera_direction = 'E'  # User can choose from 'N', 'S', 'E', or 'W'

# Compute the direction of the sun based on user choice
sun_direction = compute_sun_direction(sun_angle, camera_direction)

# Compute the dot product
dot_product = np.sum(normal_img * sun_direction, axis=2)

# Create a mask for highlighted areas
highlight_img = np.maximum(0, dot_product)

# Show results
plt.subplot(1, 2, 1)
plt.title("Normals")
plt.imshow(normal_img.astype(np.float32), cmap='gray')

plt.subplot(1, 2, 2)
plt.title("Areas Affected by Light")
#plt.imshow(highlight_img.astype(np.float32), cmap='gray')
plt.imshow(highlight_img, cmap='gray', vmin=0, vmax=1)
plt.show()

# Save the output image
output_path = './images/output_light'
output_file = f'{output_path}/{input_file}_light_{camera_direction}.png'
#output_file = f'{output_path}/sphere_light_{camera_direction}.png'

plt.imsave(output_file, highlight_img, cmap='gray')
