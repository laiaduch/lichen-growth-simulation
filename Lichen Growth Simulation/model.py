import cv2
import numpy as np


def geometric_median(img1, img2, img3):
    result = np.zeros_like(img1, dtype=np.float32)
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            result[i, j] = np.median([img1[i, j], img2[i, j], img3[i, j]])  # Mediana geométrica
    return result


def generate_probability_map(mask_img, ssao_img, rain_img):
    # Redimensionar todas las imágenes para que tengan las mismas dimensiones
    max_shape = (max(mask_img.shape[0], ssao_img.shape[0], rain_img.shape[0]),
                 max(mask_img.shape[1], ssao_img.shape[1], rain_img.shape[1]))
    mask_img = cv2.resize(mask_img, max_shape)
    ssao_img = cv2.resize(ssao_img, max_shape)
    rain_img = cv2.resize(rain_img, max_shape)

    # Normalizar imágenes
    mask_img = mask_img.astype(np.float32) / 255.0
    ssao_img = ssao_img.astype(np.float32) / 255.0
    rain_img = rain_img.astype(np.float32) / 255.0

    # Calcular mediana geométrica
    probability_map = geometric_median(mask_img, ssao_img, rain_img)

    # Normalizar mapa de probabilidad entre 0 y 1
    probability_map = (probability_map - probability_map.min()) / (probability_map.max() - probability_map.min())

    return probability_map


# Cargar las tres imágenes de entrada
mask_img = cv2.imread("./images/output_sobel/teulada1_depth.png_segmented_region.png", cv2.IMREAD_GRAYSCALE)
ssao_img = cv2.imread("./images/output_SSAO/SSAO_teulada1_depth.png", cv2.IMREAD_GRAYSCALE)
rain_img = cv2.imread("./images/output_rain/teulada1_normal.png_rain.png", cv2.IMREAD_GRAYSCALE)

# Generar el mapa de probabilidad
probability_map = generate_probability_map(mask_img, ssao_img, rain_img)

# Guardar el mapa de probabilidad como una imagen
output_path = './images/probability_map/probability_map.png'
cv2.imwrite(output_path, (probability_map * 255).astype(np.uint8))
