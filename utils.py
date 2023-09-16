import os,sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_img_name(img_dir):
    imgs_lst=os.listdir(img_dir)
    exclude=['4chan.jpg','100.jpg','608.jpg','416.jpg','320.jpg']
    fil_imgs=[]
    for img in imgs_lst:
        incldue=[img.endswith(exc) for exc in exclude]
        incldue=any(incldue)
        if not incldue:
            fil_imgs.append(img)
    return fil_imgs


def generate_parallax(rgb_image, depth_map, shift_factor=2):
    """
    Generate frames for parallax effect using RGB image and its depth map.

    :param rgb_image: Input RGB image.
    :param depth_map: Corresponding depth map (should be single channel, e.g., grayscale).
    :param shift_factor: Factor by which to shift pixels based on depth.
    :return: List of frames with parallax effect.
    """

    # Ensure depth map is single channel
    if len(depth_map.shape) > 2:
        depth_map = cv2.cvtColor(depth_map, cv2.COLOR_BGR2GRAY)

    height, width = rgb_image.shape[:2]

    # Generate multiple frames for parallax effect
    frames = []
    for shift in range(-shift_factor + 1, shift_factor + 1):
        # Create a mesh grid for shifts
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        #print(x.shape)
        x_shifted = np.clip(x + (depth_map * shift / 255.0).astype(int), 0, width - 1)
        #print(x_shifted)
        y_shifted = np.clip(y, 0, height - 1)

        # Map source pixels to destination
        frame = rgb_image[y_shifted, x_shifted]
        frames.append(frame)

    return frames

def save_parallax_as_video(parallax_frames, fps=10, output_filename='parallax_output.mp4'):
    """
    Generate a parallax effect from RGB and depth images and save it as a video.
    :parallax_frames: Frames.
    :param fps: Frames per second for the output video. Default is 10.
    :param output_filename: Name for the output video file. Default is 'parallax_output.avi'.
    """

    # Define video writer properties
    height, width, layers = parallax_frames[0].shape
    size = (width, height)
    fourcc = fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, size)

    # Write frames to video
    for frame in parallax_frames:
        out.write(frame)

    out.release()
    print(f"Video saved as {output_filename}")