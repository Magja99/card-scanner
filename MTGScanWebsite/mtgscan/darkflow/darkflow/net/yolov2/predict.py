import numpy as np
import math
import cv2
import os
import ast
import json

# from scipy.special import expit
# from utils.box import BoundBox, box_iou, prob_compare
# from utils.box import prob_compare2, box_intersection
from ...utils.box import BoundBox
from ...cython_utils.cy_yolo2_findboxes import box_constructor


def expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def _softmax(x):
    e_x = np.exp(x - np.max(x))
    out = e_x / e_x.sum()
    return out


def findboxes(self, net_out):
    # meta
    meta = self.meta
    boxes = list()
    boxes = box_constructor(meta, net_out)
    return boxes


frame = 0


def postprocess(self, net_out, im, save=True):
    """
    Takes net output, draw net_out, save to disk
    """
    outfolder = os.path.join(self.FLAGS.imgdir, "out")
    img_name = os.path.join(outfolder, "video")
    textFile = os.path.splitext(img_name)[0] + ".json"

    global frame

    if os.stat(textFile).st_size == 0:
        frame = 0
    boxes = self.findboxes(net_out)
    # meta
    meta = self.meta
    threshold = meta["thresh"]
    colors = meta["colors"]
    labels = meta["labels"]
    if type(im) is not np.ndarray:
        imgcv = cv2.imread(im)
    else:
        imgcv = im
    h, w, _ = imgcv.shape

    resultsForJSON = {"boxes": []}
    for b in boxes:
        boxResults = self.process_box(b, h, w, threshold)
        if boxResults is None:
            continue
        left, right, top, bot, mess, max_indx, confidence = boxResults
        thick = int((h + w) // 300)
        if self.FLAGS.json:
            resultsForJSON["boxes"].append(
                {
                    "frame": frame,
                    "empty": False,
                    "label": mess,
                    "confidence": float("%.2f" % confidence),
                    "topleft": {"x": left, "y": top},
                    "bottomright": {"x": right, "y": bot},
                }
            )
            clear_imgcv = imgcv.copy()

        cv2.rectangle(imgcv, (left, top), (right, bot), colors[max_indx], thick)
        cv2.putText(
            imgcv, mess, (left, top - 12), 0, 1e-3 * h, colors[max_indx], thick // 3
        )

    print(save)
    if not save:  # if video
        outfolder = os.path.join(self.FLAGS.imgdir, "out")
        img_name = os.path.join(outfolder, "video")
        if self.FLAGS.json:
            if frame % 10 == 0:
                textJSON = json.dumps(resultsForJSON)
                textFile = os.path.splitext(img_name)[0] + ".json"
                if os.stat(textFile).st_size == 0:
                    frame = 0
                with open(textFile, "r+") as f:
                    try:
                        raw = f.read()
                        file_data = json.loads(raw)
                        if resultsForJSON["boxes"] != []:
                            file_data["boxes"].append(resultsForJSON["boxes"][0])
                        else:
                            file_data["boxes"].append({"frame": frame, "empty": True})
                        f.seek(0)
                        json.dump(file_data, f, indent=4)
                    except:
                        json.dump(resultsForJSON, f, indent=4)
                if resultsForJSON["boxes"] != []:
                    cv2.imwrite(img_name + str(frame) + ".jpg", clear_imgcv)
        frame += 1
        return imgcv

    outfolder = os.path.join(self.FLAGS.imgdir, "out")
    img_name = os.path.join(outfolder, os.path.basename(im))
    if self.FLAGS.json:
        textJSON = json.dumps(resultsForJSON)
        textFile = os.path.splitext(img_name)[0] + ".json"
        with open(textFile, "w") as f:
            f.write(textJSON)
        return
    print(img_name)
    cv2.imwrite(img_name, imgcv)
