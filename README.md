# MTG Card scanner
## Getting started

1. Install CUDA Toolkit v10.0 - https://developer.nvidia.com/cuda-10.0-download-archive
2. Install requirements from requirements.txt by conda - `conda create --name <environment_name> --file requirements.txt`
3. Activate your environment with - `conda activate <environment_name>` and check if python version is 3.6

## Preparing dataset
1. Download original images of cards - `python download_images.py`
2. Download stock photos using flickscrapper https://github.com/ultralytics/flickr_scraper OR create you stock photos database by your prefered method
3. Make sure all photos are in JPEG/JPG format
4. Generate learning dataset - `python generate_learning_dataset.py`

## Training
1. Enter darkflow folder
2. `python flow --model cfg\yolov2-mtg.cfg --load bin\yolov2.weights --train --gpu 1.0 --epoch 3000 --dataset images --annotation annotations --batch 3`
    If you get `AssertionError: expect 202335260 bytes, found 203934260` change darflow/utils/loader.py 145 line: `self.offset = old_offset_value + (found_value - expected_value)`
3. Wait until the loss is ~1-5
4. Test video marking - `python flow --model cfg\yolov2-mtg.cfg --load <checkpoint from ckpt> --demo test.mp4 --saveVideo --gpu 1.0 --threshold 0.06`
