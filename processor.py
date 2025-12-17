import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

"""Image processing class - upload/redim/extract"""
class ImageProcessor:
    def __init__(self):
        self.image_path = None
        self.original_image = None # BGR image
        self.rgb_image = None # RGB image

    def load_image(self, path):
        try:
            image = cv2.imread(path)

            if image is None:
                raise ValueError("Image cannot be loaded")

            self.image_path = path
            self.original_image = image
            self.rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return True
        except Exception as e:
            print("Failed to load image:", e)
            return False

    def get_display_image(self, max_size=(400,400)):
        if self.rgb_image is None:
            return None

        h, w = self.rgb_image.shape[:2]
        scale = min(max_size[0]/w, max_size[1]/h)
        new_w = int(w*scale)
        new_h = int(h*scale)

        resized = cv2.resize(self.rgb_image, (new_w, new_h), interpolation = cv2.INTER_AREA)
        return resized

    # Using K-Means to find the dominant colours
    def extract_palette(self, n_colors=5):
        if self.rgb_image is None:
            return []

        small_image = cv2.resize(self.rgb_image, (100, 100), interpolation = cv2.INTER_AREA)
        pixels = small_image.reshape(-1, 3)

        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)

        colors = kmeans.cluster_centers_
        colors = colors.round(0).astype(int)

        return [tuple(color) for color in colors]