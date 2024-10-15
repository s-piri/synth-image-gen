# A Simple Synthetic Image Generator
A GUI simple synthetic training data generator for object detection AI, currently only support label data in YOLO format (https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format)

## Requirements
Python >= 3.8

## Installation

1. Install python requirements

```
pip install -r requirements.txt
```

Alternatively, **install.bat** can be used to install for Windows user

## Usage

```
python main.py
```
Alternatively, **launch.bat** can be used to launch the application for Windows user

1. Select Background Images
2. Select Object Image Folder
3. Choose the number of image to be generated, and parameters

Note: The object image folder must be structured as shown below:
(the subfolder names represent class indexes of the images it contain)

```bash
└───object_images
    ├───0
    │   ├───img1.png
    │   └───img2.png
    │
    └───1
        ├───img1.png
        └───img2.png
```
Note2: Preparing object images with transparent background is highly recommended

## Planned Features

- ~~Multiple object classes support~~
- ~~Randomized rotation~~
- Randomized background noise
- Object overlap prevention option
- CLI
- Segmentation data generation functionality

## Special Thanks

Thank you https://github.com/rdbende for the amazing Sun Valley Theme !
