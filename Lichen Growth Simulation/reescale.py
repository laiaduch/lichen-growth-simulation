from PIL import Image, ImageOps


def amplificar_mascara_binaria(original_path, cropped_path, output_path):
    # Obrir la imatge original i la màscara retallada
    imatge_original = Image.open(original_path)
    mascara_cropped = Image.open(cropped_path)

    # Obtenir les dimensions de la imatge original
    original_width, original_height = imatge_original.size

    # Obtenir les dimensions de la màscara retallada
    cropped_width, cropped_height = mascara_cropped.size

    # Ampliar la màscara a les dimensions de la imatge original mantenint la proporció
    scale_factor = min(original_width / cropped_width, original_height / cropped_height)
    new_size = (int(cropped_width * scale_factor), int(cropped_height * scale_factor))
    mascara_ampliada = mascara_cropped.resize(new_size, Image.NEAREST)

    # Crear una nova imatge del mateix tamany que la imatge original i enganxar-hi la màscara ampliada centrada
    imatge_final = Image.new("L", (original_width, original_height), 0)
    offset = ((original_width - new_size[0]) // 2, (original_height - new_size[1]) // 2)
    imatge_final.paste(mascara_ampliada, offset)

    # Guardar la imatge final
    imatge_final.save(output_path)


# Exemple d'ús
amplificar_mascara_binaria("./images/textures/cortezaarbre.jpg", "./images/output_light/cortezaarbre_normal.png_light_0.0.png", "./images/output_light/cortezaarbre_light_ampliada_0.png")
#amplificar_mascara_binaria("./images/textures/cortezaarbre.jpg", "./Results/Corteza Arbre/simulation_result_cortezaarbre_-90.png", "./Results/Corteza Arbre/simulation_result_cortezaarbre_ampliada_-90.png")
