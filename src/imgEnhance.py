from PIL import ImageEnhance
import numpy as np
import cv2

class Enhancer:
    def bright(self, image, brightness):
        enh_bri = ImageEnhance.Brightness(image)
        brightness = brightness
        imageBrightend = enh_bri.enhance(brightness)
        return imageBrightend

    def color(self, image, color):
        enh_col = ImageEnhance.Color(image)
        color = color
        imageColored = enh_col.enhance(color)
        return imageColored

    def contrast(self, image, contrast):
        enh_con = ImageEnhance.Contrast(image)
        contrast = contrast
        image_contrasted = enh_con.enhance(contrast)
        return image_contrasted

    def sharp(self, image, sharpness):
        enh_sha = ImageEnhance.Sharpness(image)
        sharpness = sharpness
        image_sharped = enh_sha.enhance(sharpness)
        return image_sharped

    def gamma(self, image, gamma):
        # gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
        # gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        # return cv2.LUT(image, gamma_table)
        gamma_image = np.power(image / float(np.max(image)), gamma)
        return gamma_image
