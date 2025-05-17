import numpy as np
import matplotlib.pyplot as plt

def save_ndvi_preview(ndvi_array, save_path):
    rgb_image = classify_ndvi_to_rgb(ndvi_array)
    plt.figure(figsize=(10, 10))
    plt.imshow(rgb_image)
    plt.title("NDVI com escala temática")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

def classify_ndvi_to_rgb(ndvi):
    rgb = np.zeros((ndvi.shape[0], ndvi.shape[1], 3), dtype=np.uint8)
    rgb[ndvi < 0.1] = [0, 0, 128]
    rgb[(ndvi >= 0.1) & (ndvi < 0.2)] = [255, 0, 0]
    rgb[(ndvi >= 0.2) & (ndvi < 0.3)] = [124, 94, 21]
    rgb[ndvi >= 0.3] = [16, 149, 9]
    return rgb
