import numpy as np
import matplotlib.pyplot as plt
import cv2

# Load the input depth image
input_file = 'wall3_depth.png'
depth_map = cv2.imread(f'./images/input_depth/{input_file}', cv2.IMREAD_GRAYSCALE)
img_height, img_width = depth_map.shape  # Obtain the dimensions of the image

# SSAO Parameters
num_samples = 64  # Number of samples
#radius = 10.0  # Hemisphere radius for samples
bias = 0.1  # To avoid errors due to the same depth
occlusion_map = np.zeros((img_height, img_width))
min_radius = 1  # Minimum radius
max_radius = min(img_width, img_height) / 8  # Maximum radius, 1/8 of image size

'''
# Generate random samples on the hemisphere
def generate_samples(num_samples, radius):
    samples = []
    for _ in range(num_samples):
        theta = np.random.uniform(0, np.pi / 2)  # Hemisphere angle
        phi = np.random.uniform(0, 2 * np.pi)  # Angle around the vertical axis
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)
        samples.append((x, y, z))
    return np.array(samples)
'''

# Generate random samples on 2D circle
def generate_samples(num_samples, min_radius, max_radius):
    samples = []
    for _ in range(num_samples):
        angle = np.random.uniform(0, 2 * np.pi)  # Random angle

        # Samples are evenly spread out
        rad_aux = np.random.uniform(0, 1)
        radius = np.sqrt(rad_aux) * max_radius

        x = radius * np.cos(angle)  # Coordinate x
        y = radius * np.sin(angle)  # Coordinate y

        samples.append((x, y))
    return np.array(samples)


# For each pixel, compute SSAO
for y in range(1, img_height - 1):
    for x in range(1, img_width - 1):
        occlusion = 0
        depth = depth_map[y, x]

        samples = generate_samples(num_samples, min_radius, max_radius)

        # For every sample, see if it is hidden by geometry
        for sample in samples:
            sample_x = int(x + sample[0])
            sample_y = int(y + sample[1])
            if 0 <= sample_x < img_width and 0 <= sample_y < img_height:
                sample_depth = depth_map[sample_y, sample_x]

                if sample_depth < depth - bias: # See if the sample is closer than the reference point
                    occlusion += 1

        # Normalize the result between [0, 1]
        occlusion_map[y, x] = 1 - (occlusion / num_samples)

# Show results
plt.imshow(occlusion_map, cmap='gray')
plt.title("SSAO Map")
plt.show()

# Save the output image
output_path = './images/output_SSAO'
output_file = f'{output_path}/SSAO_{input_file}'
plt.imsave(output_file, occlusion_map, cmap='gray')
