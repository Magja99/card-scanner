import json
import os
from glob import glob

import cv2
import imutils
import matplotlib.pyplot as plt
import numpy
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense, Flatten, Input, Lambda
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
)
from tqdm import tqdm

# from tensorflow.keras.utils import img_to_array


def makeKnnNumpyBig():
    labels = []
    train = []
    scryfall = os.listdir("scryfallImages")
    for img in tqdm(scryfall):
        try:
            path = os.path.join("scryfallImages", img)
            src = cv2.imread(path)
            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            target_size = (64, 64)
            dst = cv2.resize(src, target_size, interpolation=cv2.INTER_AREA)
            train.append(dst)
            labels.append(img[:-4])
        except Exception:
            continue
    labels = numpy.array(labels)
    train = numpy.array(train)
    numpy.savez("knnScryfallBig", train=train, train_labels=labels)


def makeSIFTNumpy():
    scryfall = os.listdir("scryfallImages")
    labels = []
    train = []
    sift = cv2.xfeatures2d.SIFT_create()
    for f in tqdm(scryfall):
        try:
            path = os.path.join("scryfallImages", f)
            img = cv2.imread(path)
            img = cv2.pyrDown(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, descriptors_1 = sift.detectAndCompute(img, None)
            size = (500, 500, 3)
            feature = numpy.hstack([descriptors_1])
            feature.resize(size)
            train.append(feature)
            labels.append(f[:-4])
        except Exception:
            continue
    labels = numpy.array(labels)
    train = numpy.array(train)
    numpy.savez("SIFTFeatures", train=train, train_labels=labels)


def makeVggNumpy():
    scryfall = os.listdir("scryfallImages")
    labels = []
    train = []
    vgg = VGG16(weights="imagenet", include_top=False)
    for f in tqdm(scryfall):
        try:
            path = os.path.join("scryfallImages", f)
            img = image.load_img(path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = numpy.expand_dims(x, axis=0)
            x = preprocess_input(x)
            features = vgg.predict(x)
            train.append(features.flatten())
            labels.append(f[:-4])
        except Exception:
            continue
    labels = numpy.array(labels)
    train = numpy.array(train)
    numpy.savez("tests", train=train, train_labels=labels)

makeVggNumpy()
# makeSIFTNumpy()
