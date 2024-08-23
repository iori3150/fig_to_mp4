import json
import os
import sys

import cv2


def load_config(config_file):
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

    with open(config_file, "r") as f:
        config = json.load(f)

    return config


def images_to_video(image_folder, output_video, frame_rate):
    # Get a list of image files and sort them by filename
    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]
    images.sort()

    if len(images) == 0:
        print("No images found.")
        return

    # Get the size of the first image to set the video format
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Set up the output video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    # Write images to the video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Release the video file
    video.release()
    print(f"Video file created: {output_video}")


# Load configuration from external JSON file
config_file = "config.json"
config = load_config(config_file)

# Use the settings from the configuration file
image_folder = config["image_folder"]
output_video = config["output_video"]
frame_rate = config["frame_rate"]

# Create video from images
images_to_video(image_folder, output_video, frame_rate)
