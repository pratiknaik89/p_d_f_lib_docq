
from PIL import Image
import requests
from io import BytesIO


def imageReturnNewWidth(image_path, new_height):
    response = requests.get(image_path)
    im = Image.open(BytesIO(response.content))
    height = im.size[1]
    width = im.size[0]
    return new_height * width / height

