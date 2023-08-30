import os
import xml.etree.ElementTree as ET
import shutil

# Function to rename multiple files
def rename():

    folder = "annotations"
    for count, filename in enumerate(os.listdir(folder)):
        dst = filename.replace("-", "")
        dst = dst.replace(" ", "")
        print(dst)
        src = (
            f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        )
        dst = f"{folder}/{dst}"

        # rename() function will
        # rename all the files
        os.rename(src, dst)
        mytree = ET.parse(dst)
        myroot = mytree.getroot()

        # iterating through the price values.
        for prices in myroot.iter("filename"):
            prices.text = prices.text.replace("-", "")
            prices.text = prices.text.replace(" ", "")
        mytree.write(dst)

    folder = "images"
    for count, filename in enumerate(os.listdir(folder)):
        dst = filename.replace("-", "")
        dst = dst.replace(" ", "")
        print(dst)
        src = (
            f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        )
        dst = f"{folder}/{dst}"

        # rename() function will
        # rename all the files
        os.rename(src, dst)


def delete_ann():

    folder_ann = "annotations"
    folder_img = "images"
    for count, filename in enumerate(os.listdir(folder_ann)):
        jpg = filename.replace(".xml", ".jpg")
        img_f = (
            f"{folder_img}/{jpg}"  # foldername/filename, if .py file is outside folder
        )
        ann_f = f"{folder_ann}/{filename}"
        if not os.path.isfile(img_f):
            print(img_f, ann_f)
            os.remove(ann_f)


def divide():
    folder_ann = "annotations"
    folder_img = "images"
    folder_organn = "org_annotations"
    folder_orgimg = "org_images"

    for count, filename in enumerate(os.listdir(folder_organn)):
        jpg = filename.replace(".xml", ".jpg")
        img_f = f"{folder_orgimg}/{jpg}"
        ann_f = f"{folder_organn}/{filename}"
        dest_img = f"{folder_img}/{jpg}"
        dest_ann = f"{folder_ann}/{filename}"
        if "gen" not in jpg and os.path.isfile(img_f):
            shutil.move(img_f, dest_img)
            shutil.move(ann_f, dest_ann)


# divide()
rename()
# import tensorflow as tf
# from tensorflow.python.client import device_lib

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# device_lib.list_local_devices()
