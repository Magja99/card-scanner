#! /usr/bin/env python

import sys
from darkflow.cli import cliHandler
import os
from moviepy.editor import VideoFileClip


def run(video):
    file_to_delete = open(
        "../MTGScanWebsite/sample_img/out/video.json",
        "w",
    )
    file_to_delete.close()
    for file in os.scandir(
        "../MTGScanWebsite/sample_img/out/"
    ):
        if file.name.endswith(".jpg"):
            os.remove(file.path)
    args = [
        "flow",
        "--model",
        "../MTGScanWebsite/mtgscan/darkflow/cfg/yolov2-mtg.cfg",
        "--load",
        "1332",
        "--demo",
        video,
        "--saveVideo",
        "--gpu",
        "1.0",
        "--threshold",
        "0.06",
        "--json",
    ]
    cliHandler(args)
    os.remove(
        "../MTGScanWebsite/mtgscan/media/video.mp4"
    )

    input_path = "../MTGScanWebsite/video.avi"

    output_path = (
        "../MTGScanWebsite/mtgscan/media/video.mp4"
    )

    video_clip = VideoFileClip(input_path)

    video_clip.write_videofile(output_path, codec="libx264")

    video_clip.close()
