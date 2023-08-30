# scripts/createDatabase.py
import os
import tqdm
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MTGScanWebsite.settings")
from .models import Card



def make_new_name(name):
    new_name = "".join(ch for ch in name if ch.isalnum())
    new_name = new_name.replace(" ", "") + ".jpg"
    return new_name


def aaa():
    with open("../../cardsImagesUris.json", "r") as file:
        data = json.load(file)
        for i in data:
            network_name = make_new_name(i["name"])
            card = Card.objects.create(name=i["name"], networkName=network_name)
