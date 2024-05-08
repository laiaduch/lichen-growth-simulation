import cv2
import numpy as np
import matplotlib.pyplot as plt


def region_growing(img, seed, threshold, edge_mask=None):
    rows, cols = img.shape
    region = np.zeros_like(img, dtype=np.uint8)
    visited = np.zeros_like(img, dtype=np.uint8)
    stack = [seed]

    while len(stack) > 0:
        current_point = stack.pop()
        x, y = current_point

        if (x < 0 or x >= rows) or (y < 0 or y >= cols):
            continue

        if visited[x, y]:
            continue

        if edge_mask is not None and edge_mask[x, y]:
            continue

        if abs(img[x, y] - img[seed]) < threshold:
            region[x, y] = 255
            visited[x, y] = 1

            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

    return region


if __name__ == "__main__":

    input_file = 'tree2_depth.png'

    # Read input image
    input_image = cv2.imread(f'./images/input_depth/{input_file}', cv2.IMREAD_GRAYSCALE)

    # Apply Sobel edge detection
    sobel_x = cv2.Sobel(input_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(input_image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_mag = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

    # Threshold Sobel magnitude to obtain edge mask
    sobel_edge_mask = np.uint8(sobel_mag > 10)  # Adjust threshold as needed

    # Define seed point (you may choose this interactively)
    seed_point = (500, 250)

    # Perform region growing
    threshold_value = 100  # Adjust threshold as needed
    segmented_region = region_growing(input_image, seed_point, threshold_value, sobel_edge_mask)

    '''# Display results
    cv2.imshow("Original Image", input_image)
    cv2.imshow("Sobel Edge Mask", sobel_edge_mask * 255)
    cv2.imshow("Segmented Region", segmented_region)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

    # Show results
    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(input_image.astype(np.float32), cmap='gray')

    plt.subplot(1, 3, 2)
    plt.title("Sobel Edge Mask")
    plt.imshow(sobel_edge_mask * 255, cmap='gray')

    plt.subplot(1, 3, 3)
    plt.title("Segmented Region")
    plt.imshow(segmented_region, cmap='gray')
    plt.show()

    # Save the output images
    output_directory = './images/output_sobel'
    cv2.imwrite(f'{output_directory}/{input_file}_sobel_edge_mask.png', sobel_edge_mask * 255)
    cv2.imwrite(f'{output_directory}/{input_file}_segmented_region.png', segmented_region)
