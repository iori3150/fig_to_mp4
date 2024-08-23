import os

import cv2


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


# Example usage
image_folder = "./"  # Directory where images are stored
output_video = "output.mp4"  # Name of the output video file
frame_rate = 5

images_to_video(image_folder, output_video, frame_rate)
