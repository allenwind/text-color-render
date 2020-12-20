from PIL import ImageFont
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from textcolor import hexcolors, hex_lenght

class ImageFontTransformer:

    def __init__(self, file="fonts/STKAITI.TTF", size=30, pad_size=32):
        self.file = file
        self.size = size
        self.pad_size = pad_size
        self.font = ImageFont.truetype(file, size=size)

    def transform(self, c):
        return self.char_to_glyph(c)

    def char_to_glyph(self, c):
        mask = self.font.getmask(c)
        size = mask.size[::-1]
        glyce = np.asarray(mask).reshape(size)
        # glyce[glyce != 0] = 255
        return self.pad_array(glyce)[:,:,np.newaxis] / 255

    def pad_array(self, array):
        # pad to center with same shape
        shape = array.shape
        a1 = (self.pad_size - shape[0]) // 2
        a2 = (self.pad_size - shape[0]) - a1

        b1 = (self.pad_size - shape[1]) // 2
        b2 = (self.pad_size - shape[1]) - b1
        array = np.pad(
            array,
            [(a1, a2), (b1, b2)],
            mode="constant",
            constant_values=0
        )
        return array

tr = ImageFontTransformer()
def render_color_image(text, ws):
    ws = np.array(ws)
    ws = (ws - np.min(ws)) / (np.max(ws) - np.min(ws)) * 0.99
    images = []
    for string, w in zip(text, ws):
        i = int(w * hex_lenght)
        hexcode = hexcolors[i]
        rgb = matplotlib.colors.hex2color(hexcode)
        image = tr.transform(string)
        image = np.concatenate([image * c for c in rgb], axis=-1)
        images.append(image)
    image = np.concatenate(images, axis=-2)
    return image

if __name__ == "__main__":
    # for testing
    text = "NLP的魅力在于不断探索"
    image = render_color_image(text, np.arange(len(text)))
    plt.imshow(image)
    plt.show()
