from PIL import Image, ImageDraw
import os
import random
from generate_xml import make_xml
from math import *

scryfall = os.listdir("scryfallImages")
stockPhotos = os.listdir("stockPhotos")
s = "genA"


def next_batch(char):
    return "gen" + chr((ord(char.upper()) + 1 - 65) % 26 + 65)


def rotate_image(img):
    l_r = random.randint(1, 2)
    if l_r == 1:
        img = img.rotate(random.randint(340, 360), expand=1)
    else:
        img = img.rotate(random.randint(0, 20), expand=1)
    return img


for j in range(4):
    for it, stockPhoto in enumerate(stockPhotos):
        background = Image.open(f"stockPhotos/{stockPhoto}")

        background_width, background_height = background.size
        max_size = floor(max(background_width, background_height) * 0.3)
        draw = ImageDraw.Draw(background)
        file = random.choice(scryfall)
        topl = []
        botr = []
        try:
            image_obj = Image.open("scryfallImages/" + file).convert("RGBA")
            image_width, image_height = image_obj.size
            if image_width > max_size or image_height > max_size:
                if image_width > image_height:
                    ratio = max_size / float(image_width)
                    new_height = int(image_height * ratio)
                    image_obj = image_obj.resize((max_size, new_height))
                else:
                    ratio = max_size / float(image_height)
                    new_width = int(image_width * ratio)
                    image_obj = image_obj.resize((new_width, max_size))
            position = (
                random.randint(0, background_width - image_obj.width),
                random.randint(0, background_height - image_obj.height),
            )
            image_obj = rotate_image(image_obj)
            background.paste(image_obj, position, image_obj)

            coordinates = [
                position[0],
                position[1],
                position[0] + image_obj.width,
                position[1] + image_obj.height,
            ]
            topl.append(
                (
                    position[0],
                    position[1],
                )
            )
            botr.append((position[0] + image_obj.width, position[1] + image_obj.height))
            name = s + str(it)
            background.save(f"MTGScanWebsite/mtgscan/darkflow/images/{name}.jpg")

            make_xml(
                "images",
                f"{name}.jpg",
                ["mtgCard"],
                topl,
                botr,
                "MTGScanWebsite/mtgscan/darkflow/annotations",
                f"MTGScanWebsite/mtgscan/darkflow/images/{name}.jpg",
            )
        except Exception:
            continue
    s = next_batch(s[-1])
