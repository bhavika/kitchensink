from keras_preprocessing.image import load_img, img_to_array
import numpy as np


class Image:
    def __init__(self, *args, **kwargs):
        self.path = args[0]
        self.original = load_img(self.path)

    def resize_to_max(self, n):
        """
    Resize self.original so its longest side has n pixels (maintain proportion)
    """
        w, h = self.original.size
        size = (n, int(n * h / w)) if w > h else (int(n * w / h), n)
        return img_to_array(self.original.resize(size))

    def resize_to_height(self, height):
        """
    Resize self.original into an image with height h and proportional width
    """
        w, h = self.original.size
        if (w / h * height) < 1:
            resizedwidth = 1
        else:
            resizedwidth = int(w / h * height)
        size = (resizedwidth, height)
        return img_to_array(self.original.resize(size))

    def resize_to_square(self, n, center=False):
        """
    Resize self.original to an image with nxn pixels (maintain proportion)
    if center, center the colored pixels in the square, else left align
    """
        a = self.resize_to_max(n)
        h, w, c = a.shape
        pad_lr = int((n - w) / 2)  # left right pad
        pad_tb = int((n - h) / 2)  # top bottom pad
        b = np.zeros((n, n, 3))
        if center:
            b[pad_tb : pad_tb + h, pad_lr : pad_lr + w, :] = a
        else:
            b[:h, :w, :] = a
        return b
