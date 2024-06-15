from PIL import Image
import numpy as np
import os

# Paths to the images
foreground_path = "./images/textures/lichen.jpg"
background_path = "./images/textures/cortezaarbre.jpg"
alpha_path = "./Results/Corteza Arbre/simulation_result_cortezaarbre_ampliada_0.png"
light_map_path = "./images/output_light/cortezaarbre_light_ampliada_0.png"  # Path to the light map
output_directory = "./Lichen"
#output_image_path = os.path.join(output_directory, "simulation_cortezaarbre_texture_-90_nollum.png")
output_image_path = os.path.join(output_directory, "simulation_pedra_texture_0.png")

# Read the images
foreground = Image.open(foreground_path).convert("RGB")
background = Image.open(background_path).convert("RGB")
alpha = Image.open(alpha_path).convert("L")  # Load alpha as grayscale
light_map = Image.open(light_map_path).convert("L")  # Load light map as grayscale

#Resize lichen image
foreground = foreground.resize((background.width, background.height))

# Get dimensions of background
bg_width, bg_height = background.size

# Get dimensions of foreground
fg_width, fg_height = foreground.size

# Calculate cropping box (center crop)
left = (fg_width - bg_width) // 2
top = (fg_height - bg_height) // 2
right = left + bg_width
bottom = top + bg_height

# Crop the foreground image
foreground_cropped = foreground.crop((left, top, right, bottom))

# Ensure alpha mask and light map are the same size as the background
alpha = alpha.resize((bg_width, bg_height))
light_map = light_map.resize((bg_width, bg_height))

# Convert images to numpy arrays
foreground_cropped = np.array(foreground_cropped).astype(float)
background = np.array(background).astype(float)
alpha = np.array(alpha).astype(float) / 255  # Normalize alpha to range [0, 1]
light_map = np.array(light_map).astype(float) / 255  # Normalize light map to range [0, 1]

# Apply the light map to the foreground
foreground_cropped = foreground_cropped * light_map[..., np.newaxis]

# Multiply the foreground with the alpha matte
foreground_cropped = np.multiply(alpha[..., np.newaxis], foreground_cropped)

# Multiply the background with (1 - alpha)
background = np.multiply(1.0 - alpha[..., np.newaxis], background)

# Add the masked foreground and background
out_image = np.add(foreground_cropped, background).astype(np.uint8)

# Convert the result back to an image
out_image = Image.fromarray(out_image)

# Save result
out_image.save(output_image_path)

# Display image
out_image.show()
