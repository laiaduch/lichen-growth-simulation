import numpy as np
import tensorflow as tf
import cv2

# Define the neural network to extract the normals
def build_model(input_shape):
    model = tf.keras.Sequential([
        # Define neural network layers
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=input_shape),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
        tf.keras.layers.Conv2D(2, kernel_size=(3, 3), activation='tanh', padding='same')  # Output: 2 channels (x,y components)
    ])
    return model

# Load and preprocess the input image
def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path)
   # image = cv2.resize(image, (512, 512 ))  # Resize
    image = image.astype(np.float32) / 255.0  # Normalize the pixels values between 0 and 1
    return image

# Visualize the normals into a new image
def visualize_normals(normals):

    norm = np.sqrt(np.sum(normals ** 2, axis=-1, keepdims=True)) # Scale the normals so they have a length of 1 in 3D space
    normals /= norm + 1e-8
    # Compute cartesian coordinates
    x = normals[:, :, 0]
    y = normals[:, :, 1]
    z = np.sqrt(np.maximum(0, 1 - x ** 2 - y ** 2))  # z = sqrt(max(0, 1 - x^2 - y^2))

    output_image = np.stack([x, y, z], axis=-1) # Map the color coordinates

    # Normalize the output image to the range [0, 1]
    output_image = (output_image + 1) / 2

    return (output_image + 1) * 127.5  # Scale into [0, 255]


# image_path = './images/textures/test.png'
input_image = load_and_preprocess_image('./images/textures/test.png')

# Build the model
input_shape = input_image.shape
model = build_model(input_shape)
#print(input_shape)

# Predict normals
normals_map = model.predict(np.expand_dims(input_image, axis=0))[0]

output_image = visualize_normals(normals_map)

# Apply colormap
gray_image = cv2.cvtColor(output_image.astype(np.uint8), cv2.COLOR_RGB2GRAY) # Grayscale image
jet_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_JET)

cv2.imshow('extracted normals', jet_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
