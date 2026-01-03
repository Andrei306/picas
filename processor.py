import cv2
from sklearn.cluster import KMeans

"""
@file processor.py
@brief Core logic for image processing and K-Means clustering (upload/redim/extract).
"""

class ImageProcessor:
    """
    @brief Handles image loading, resizing, and color extraction logic.
    """
    def __init__(self):
        """
        @brief Initializes the processor with empty image states.
        """
        self.image_path = None
        self.original_image = None # BGR image
        self.rgb_image = None # RGB image

    """
    @brief Loads an image via OpenCV and converts it from BGR to RGB.

    @param path - String path to the image file.
    @return bool - True if loaded successfully, False otherwise.
    """
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

    """
    @brief Resizes the loaded image for GUI display, maintaining aspect ratio.

    @param max_size - Tuple (width, height) defining maximum dimensions.
    @return numpy.ndarray - Resized image array or None if no image loaded.
    """
    def get_display_image(self, max_size=(400,400)):
        if self.rgb_image is None:
            return None

        h, w = self.rgb_image.shape[:2]
        scale = min(max_size[0]/w, max_size[1]/h)
        new_w = int(w*scale)
        new_h = int(h*scale)

        resized = cv2.resize(self.rgb_image, (new_w, new_h), interpolation = cv2.INTER_AREA)
        return resized

    """
    @brief Extracts dominant colors using K-Means clustering.

    @param n_colors - Number of colors to extract (default 5).
    @return list - List of RGB tuples representing dominant colors.
    """
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