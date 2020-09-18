
from PIL import Image   


def imageReturnNewWidth(image_path, new_height):
    im = Image.open(image_path)
    height = im.size[1]
    width = im.size[0]
    return new_height * width / height
