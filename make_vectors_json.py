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
    # labels = []
    # train = []
    # vgg = VGG16(weights="imagenet", include_top=False)
    # for f in tqdm(scryfall):
    #     try:
    #         path = os.path.join("scryfallImages", f)
    #         img = image.load_img(path, target_size=(224, 224))
    #         x = image.img_to_array(img)
    #         x = numpy.expand_dims(x, axis=0)
    #         x = preprocess_input(x)
    #         features = vgg.predict(x)
    #         train.append(features.flatten())
    #         labels.append(f[:-4])
    #     except Exception:
    #         continue
    # labels = numpy.array(labels)
    # train = numpy.array(train)
    # numpy.savez("tests", train=train, train_labels=labels)

    model = VGG16(weights="imagenet", include_top=True)

    # Załaduj i przetwórz obraz
    img_path = "scryfallImages\SirenLookout.jpg"  # Podmień na ścieżkę do swojego obrazu
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = numpy.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Wybierz warstwy, z których chcesz wizualizować cechy
    layer_names = [
        "block1_conv1",
        "block2_conv1",
        "block3_conv1",
        "block4_conv1",
        "block5_conv1",
    ]

    # Utwórz modele dla każdej warstwy
    layer_outputs = [model.get_layer(name).output for name in layer_names]
    activation_model = Model(inputs=model.input, outputs=layer_outputs)

    # Pobierz aktywacje
    activations = activation_model.predict(img_array)

    # Wizualizuj cechy dla pierwszego kanału każdej warstwy
    for i, (layer_name, layer_activation) in enumerate(zip(layer_names, activations)):
        # Wybierz pierwszy kanał aktywacji
        first_channel_activation = layer_activation[0, :, :, 0]

        plt.figure(figsize=(4, 4))
        plt.title(f"{layer_name} - kanał 1")
        plt.imshow(first_channel_activation, cmap="viridis")
        plt.axis("off")
        plt.savefig(f"{layer_name}_activation_{i}.jpg")
    plt.show()


makeVggNumpy()
# makeSIFTNumpy()

#przykład że knn działa
#zrobilismy zamiast zrobilam
#nagranie filmu user experience bez głosu
