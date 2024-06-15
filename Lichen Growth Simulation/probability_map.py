from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the input images
rain_image = Image.open("./images/output_rain/cortezaarbre_normal.png_rain.png").convert("L")
ssao_image = Image.open("./images/output_SSAO/Blurred_SSAO_cortezaarbre_depth.png").convert("L")
direct_light_image = Image.open("./images/output_light/cortezaarbre_normal.png_light_-90.0.png").convert("L")
mask_image = Image.open("./images/output_sobel/cortezaarbre_depth.png_segmented_region.png").convert("L")

# Obtain the size of input image
image_size = rain_image.size

# Resize binary mask
mask_image_resized = mask_image.resize(image_size, Image.NEAREST)

# Convert the images into numpy arrays
rain_array = np.array(rain_image)
ssao_array = np.array(ssao_image)
direct_light_array = np.array(direct_light_image)
mask_array = np.array(mask_image_resized )

# Calculate the inverse of the direct light array
inverse_direct_light_array = 255 - direct_light_array

# For each pixel, find the minimum value of the environment images using the inverted direct light
min_array = np.minimum(np.minimum(rain_array, ssao_array), inverse_direct_light_array)

# Multiply by binary mask
probability_map_array = min_array * (mask_array / 255)  # Normalize binary mask

# Convert the results into images
probability_map_image = Image.fromarray(np.uint8(probability_map_array))

# Show results
plt.title("Probability Map")
plt.imshow(probability_map_image, cmap='gray')
plt.show()

# Save the results
probability_map_image.save("./images/probability_map/probability_map_cortezaarbre_-90.png")

print(probability_map_image.size)