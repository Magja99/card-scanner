import os
import json
import cv2
import numpy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
import imutils
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense, Flatten, Input, Lambda
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
)


def pick_cards(markedCardsFolder):
    print("Picking best cards locations")
    cardsJsons = []
    jsonFile = os.path.join(markedCardsFolder, "video.json")
    with open(jsonFile, "r") as jf:
        data = json.load(jf)
        newCard = True
        bestConfidence = -1
        bestGuess = None
        for i in data["boxes"]:
            if i["empty"] == True:
                newCard = True
                if bestGuess != None:
                    cardsJsons.append(bestGuess)
                    bestGuess = None
                    bestConfidence = -1
            elif newCard == True and i["empty"] == False:
                newCard = False
                bestConfidence = i["confidence"]
                bestGuess = i
            elif newCard == False:
                if i["confidence"] > bestConfidence:
                    bestConfidence = i["confidence"]
                    bestGuess = i
        if bestGuess != None:
            cardsJsons.append(bestGuess)
    return cardsJsons


def makeVec(frames, dir):
    print("Making feature vector out of the cards")
    vec = []
    vgg = VGG16(weights="imagenet", include_top=False)
    for i in frames:
        print(i)
        path = os.path.join(dir, "video" + str(i["frame"]) + ".jpg")
        card = cv2.imread(path)
        y, x, h, w = (
            i["topleft"]["x"],
            i["topleft"]["y"] + 20,
            i["bottomright"]["x"],
            i["bottomright"]["y"] - 20,
        )
        cropped = card[x:w, y:h]
        cv2.imwrite("img.jpg", cropped)
        ## Pixels
        # cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        # target_size = (64,64)
        # dst = cv2.resize(cropped, target_size, interpolation = cv2.INTER_AREA)
        # dst = dst.flatten()
        # vec.append(dst)

        ##VGG
        img = load_img("img.jpg", target_size=(224, 224))
        x = img_to_array(img)
        x = numpy.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = vgg.predict(x)
        vec.append(features.flatten())

    vec = numpy.array(vec)
    print(vec.shape)
    print("Vector prepared")
    return vec


def transform_data(js):
    with open(js, "r+") as f:
        print("Reading all the cards data")
        raw = f.read()
        file_data = json.loads(raw)
        data = []
        labels = []
        print("Transforming all the cards...")
        for img in tqdm(file_data["vectors"]):
            labels.append(img["name"])
            data.append(numpy.array(img["features"]))
        data = numpy.array(data)
        labels = numpy.array(labels)
        return labels, data


def guess_a_card_KNN(vec):
    with numpy.load("../VGG16Features.npz") as data:
        train = data["train"]
        train_labels = data["train_labels"]
        print(train.shape, train_labels.shape)
        (trainX, testX, trainY, testY) = train_test_split(
            train, train_labels, test_size=0.25
        )
        print(trainX.shape, trainY.shape, vec.shape)
        print("Entering training...")
        model = KNeighborsClassifier(
            n_neighbors=1, n_jobs=-1, metric="cosine", algorithm="brute"
        )
        model.fit(train, train_labels)
        return model.predict(vec)


def guess_a_card_SIFT(frames, dir):
    ans = []
    sift = cv2.xfeatures2d.SIFT_create()
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    scryfallSIFTVectors = os.listdir("../siftScryfall")
    for i in frames:
        path = os.path.join(dir, "video" + str(i["frame"]) + ".jpg")
        image = cv2.imread(path)
        y, x, h, w = (
            i["topleft"]["x"],
            i["topleft"]["y"],
            i["bottomright"]["x"],
            i["bottomright"]["y"],
        )
        cropped = image[x:w, y:h]
        cv2.imwrite(os.path.join(dir, "cropped.jpg"), cropped)
        cropped = cv2.imread(os.path.join(dir, "cropped.jpg"))
        cropped = cv2.pyrDown(cropped)
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, descriptors_1 = sift.detectAndCompute(cropped, None)
        max = -1
        pos = None
        for f in tqdm(scryfallSIFTVectors):
            vec = numpy.load(os.path.join("../siftScryfall", f))
            matches = bf.match(descriptors_1, vec["info1"])
            if len(matches) > max:
                max = len(matches)
                pos = f
                print(pos, max)
        ans.append(pos)
    print(ans)


def guess_cards(markedCardsFolder="sample_img/out"):
    bestFrames = pick_cards(markedCardsFolder)
    print("guessing cards")
    vec = makeVec(bestFrames, markedCardsFolder)
    return guess_a_card_KNN(vec)
