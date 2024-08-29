import json
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog
import cv2

def load_config(config_file):
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

    with open(config_file, "r") as f:
        config = json.load(f)

    return config

def get_relative_paths():
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select multiple directories
    selected_dirs = []
    while True:
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            selected_dirs.append(selected_dir)
        else:
            break

    # Get the absolute paths of the selected directories
    absolute_paths = [os.path.abspath(dir) for dir in selected_dirs]

    # Get the base directory (the directory where the script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Calculate the relative paths
    relative_paths = [os.path.relpath(path, base_dir) for path in absolute_paths]

    return relative_paths

def images_to_video(image_folder, output_video, frame_rate):
    # Get a list of image files and sort them by filename
    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]
    images.sort()

    if len(images) == 0:
        print(f"No images found in {image_folder}.")
        return

    # Get the size of the first image to set the video format
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    # Start time for progress tracking
    start_time = time.time()

    # Write images to the video
    total_images = len(images)
    for idx, image in enumerate(images):
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

        # Progress calculation
        current_time = time.time()
        elapsed_time = current_time - start_time
        percentage_complete = (idx + 1) / total_images * 100
        estimated_total_time = elapsed_time / (idx + 1) * total_images
        estimated_time_remaining = estimated_total_time - elapsed_time

        # Log progress
        print(
            f"Processing file: {image} | "
            f"Progress: {percentage_complete:.2f}% | "
            f"Elapsed time: {elapsed_time:.2f}s | "
            f"Estimated time remaining: {estimated_time_remaining:.2f}s"
        )

    # Release the video file
    video.release()
    print(f"Video saved as {output_video}")

def main():
    # Load configuration
    config = load_config("config.json")

    # Get relative paths of selected directories
    relative_paths = get_relative_paths()

    # Process each directory
    for i, relative_path in enumerate(relative_paths):
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        
        # Determine output directory based on config["output video"]
        if config["output_video"] == 0:
            output_dir = "./"
        elif config["output_video"] == 1:
            output_dir = os.path.join(image_folder, "movie")
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            raise ValueError("Invalid value for 'output video' in config. Must be 0 or 1.")
        
        
        output_video = os.path.join(output_dir, f"output_video_{i+1}.mp4")
        frame_rate = config["frame_rate"]
        images_to_video(image_folder, output_video, frame_rate)

if __name__ == "__main__":
    main()