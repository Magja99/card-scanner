from turtle import down
import requests
import json
import pprint


def make_new_name(name, n):
    new_name = "".join(ch for ch in name if ch.isalnum())
    new_name = "scryfallImages/" + new_name.replace(" ", "") + n + ".jpg"
    return new_name


def download_images():
    with open("cardsImagesUris.json", "r") as file:
        k = 0
        data = json.load(file)
        for i in data:
            print(k)
            n = ""
            for j in i["image_uris"]:
                img = requests.get(j).content
                jpgName = make_new_name(i["name"], n)
                with open(jpgName, "wb") as handler:
                    handler.write(img)
                n = "2"
            k += 1


download_images()
