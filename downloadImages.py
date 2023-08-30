from turtle import down
import requests
import json
import pprint


def make_json():
    res = []
    with open("cards.json", "r", encoding="utf8") as file:
        data = json.load(file)
        for i in data:
            if i["image_status"] == "highres_scan":
                cards = {}
                print(i["name"])
                cards["name"] = i["name"]
                if not "image_uris" in i:
                    cards["faces"] = len(i["card_faces"])
                    cards["image_uris"] = []
                    for j in i["card_faces"]:
                        cards["image_uris"].append(j["image_uris"]["large"])
                        print(j["image_uris"]["large"])
                else:
                    cards["faces"] = 1
                    cards["image_uris"] = [i["image_uris"]["large"]]
                    print(i["image_uris"]["large"])
                res.append(cards)
    with open("cardsImagesUris.json", "w") as outfile:
        json.dump(res, outfile)
    print(len(res))


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


make_json()
download_images()
