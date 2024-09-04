import json
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Spinbox, Button, Radiobutton, IntVar, StringVar
import cv2

def get_relative_paths_and_frame_rate():
    global listbox, frame_rate_spinbox, output_mode_var, root, progress_label, result

    def add_directory():
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            listbox.insert(tk.END, selected_dir)

    def remove_directory():
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices):
            listbox.delete(index)

    def on_done():
        global listbox ,result
        selected_dirs = listbox.get(0, tk.END)
        absolute_paths = [os.path.abspath(dir) for dir in selected_dirs]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        relative_paths = [os.path.relpath(path, base_dir) for path in absolute_paths]
        try:
            frame_rate = int(frame_rate_spinbox.get())
            if frame_rate <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for frame rate.")
            return
        output_mode = bool(output_mode_var.get())
        result = (relative_paths, frame_rate, output_mode)
        root.quit()

    root = tk.Tk()
    root.title("Select Directories and Frame Rate")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    listbox = Listbox(frame, selectmode=tk.MULTIPLE, width=100, height=15)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    v_scrollbar = Scrollbar(frame, orient=tk.VERTICAL)
    v_scrollbar.config(command=listbox.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=v_scrollbar.set)

    h_scrollbar = Scrollbar(frame, orient=tk.HORIZONTAL)
    h_scrollbar.config(command=listbox.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    listbox.config(xscrollcommand=h_scrollbar.set)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    add_button = tk.Button(button_frame, text="Add Directory", command=add_directory)
    add_button.pack(side=tk.LEFT, padx=5)

    remove_button = tk.Button(button_frame, text="Remove Selected", command=remove_directory)
    remove_button.pack(side=tk.LEFT, padx=5)

    frame_rate_label = tk.Label(root, text="Frame Rate:")
    frame_rate_label.pack(pady=5)

    frame_rate_var = StringVar(value="24")
    frame_rate_spinbox = Spinbox(root, from_=1, to=60, textvariable=frame_rate_var, width=3)
    frame_rate_spinbox.pack(pady=5)

    output_mode_var = IntVar()
    output_mode_var.set(0)

    output_mode_label = tk.Label(root, text="Output Mode:")
    output_mode_label.pack(pady=5)

    output_mode_frame = tk.Frame(root)
    output_mode_frame.pack(pady=5)

    radio_button_0 = Radiobutton(output_mode_frame, text="Export src folder", variable=output_mode_var, value=0)
    radio_button_0.pack(side=tk.LEFT, padx=5)

    radio_button_1 = Radiobutton(output_mode_frame, text="Export img folder", variable=output_mode_var, value=1)
    radio_button_1.pack(side=tk.LEFT, padx=5)

    done_button = tk.Button(root, text="Done", command=lambda: on_done())
    done_button.pack(pady=5)

    progress_label = tk.Label(root, text="")
    progress_label.pack(pady=5)

    root.mainloop()

    return result

def images_to_video(image_folder, output_video, frame_rate, progress_label):
    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]
    images.sort()

    if len(images) == 0:
        print(f"No images found in {image_folder}.")
        return

    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

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
        progress_label.config(
            text=(
                f"Processing file: {image} | "
                f"Progress: {percentage_complete:.2f}% | "
                f"Elapsed time: {elapsed_time:.2f}s | "
                f"Estimated time remaining: {estimated_time_remaining:.2f}s"
            )
        )
        progress_label.update()

    video.release()
    progress_label.config(text=f"Video saved as {output_video}")

def main():
    relative_paths, frame_rate, output_mode = get_relative_paths_and_frame_rate()

    for i, relative_path in enumerate(relative_paths):
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        
        if output_mode:
            output_dir = os.path.join(image_folder, "movie")
        else:
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movie")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_video = os.path.join(output_dir, f"output_video_{i+1}.mp4")
        images_to_video(image_folder, output_video, frame_rate, progress_label)

if __name__ == "__main__":
    main()