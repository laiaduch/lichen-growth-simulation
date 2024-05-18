import numpy as np
import matplotlib.pyplot as plt
import cv2

# Generate random samples on 2D circle
def generate_samples(num_samples, max_radius):
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

# Compute Ambient Occlusion map
def compute_ssao(normal_image, depth_image, num_samples, max_radius):
    height, width = normal_image.shape[:2]
    occlusion_map = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            normal = normal_image[y, x]
            depth = depth_image[y, x]

            occlusion = 0.0

            samples = generate_samples(num_samples, max_radius)

            for sample in samples:
                sample_x = int(x + sample[0])
                sample_y = int(y + sample[1])

                if sample_x < 0 or sample_x >= width or sample_y < 0 or sample_y >= height:
                    continue

                sample_depth = depth_image[sample_y, sample_x]
                sample_normal = normal_image[sample_y, sample_x]

                # Compute occlusion factor using dot product
                dot_product = np.dot(normal, sample_normal)
                occlusion += float(sample_depth <= depth) * max(0, dot_product)

            occlusion /= num_samples
            occlusion_map[y, x] = 1 - (occlusion/num_samples)

    return occlusion_map


# Input images (normals and depth)
input_normal = 'wall_normal.png'
normal_image = cv2.imread(f'./images/input_normal/{input_normal}')
img_width, img_height, _ = normal_image.shape

input_depth = 'wall_depth.png'
depth_image = cv2.imread(f'./images/input_depth/{input_depth}', cv2.IMREAD_GRAYSCALE)

# Resize depth image
depth_image = cv2.resize(depth_image, (img_width, img_height), interpolation=cv2.INTER_LINEAR)

# SSAO Parameters
num_samples = 64
max_radius = min(img_width, img_height) / 8  # Maximum radius, 1/8 of image size

# Compute Ambient Occlusion Map
occlusion_map = compute_ssao(normal_image, depth_image, num_samples, max_radius)

# Apply blur filter to smooth the occlusion map
#occlusion_map_blur = cv2.blur(occlusion_map, (0, 0))  # Adjust the kernel size as needed

# Show Results
plt.imshow(occlusion_map, cmap='gray')
plt.title("Blurred SSAO Map")
plt.show()

# Save the output image
output_path = './images/output_SSAO'
output_file = f'{output_path}/Blurred_SSAO_{input_depth}'
plt.imsave(output_file, occlusion_map, cmap='gray')