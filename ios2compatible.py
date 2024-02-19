# Description: This script converts HEIC images to JPEG and MOV videos to MP4.
# WSL2

from PIL import Image
import pyheif
from tqdm import tqdm
import os, glob
from moviepy.editor import VideoFileClip

DIR_PATH = "input ur directory path here"

def convert_heic_to_jpg(heic_path):
    # Create the new filename by replacing the '.heic' extension with '.jpg'
    new_name = os.path.splitext(heic_path)[0] + ".jpg"
    
    # Read the HEIC file
    heif_file = pyheif.read(heic_path)
    
    # Convert the HEIC image data to PIL Image
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Save the image as JPEG
    image.save(new_name, "JPEG")
    print(f"{heic_path} converted to {new_name}")

    # Delete the original HEIC file
    os.remove(heic_path)


def convert_mov_to_mp4(mov_path):
    # Create the new filename by replacing the '.mov' extension with '.mp4'
    new_name = os.path.splitext(mov_path)[0] + ".mp4"
    
    # Load the video clip
    video_clip = VideoFileClip(mov_path)
    
    # Get video information
    width = video_clip.size[0]
    height = video_clip.size[1]
    rotation = video_clip.rotation
    fps = video_clip.fps
    duration = video_clip.duration
    
    #print("Video Information:", width, height, rotation, fps, duration)
    
    # Convert MOV to MP4 and save
    if rotation == 90:
        video_clip.write_videofile(new_name, codec='libx264', ffmpeg_params=["-vf", f"scale={height}:{width}"])
    else:
        video_clip.write_videofile(new_name, codec='libx264', ffmpeg_params=["-vf", f"scale={width}:{height}"])
    
    #print(f"{mov_path} converted to {new_name}")

    # Delete the original MOV file
    os.remove(mov_path)

def main():
    print("Starting the conversion process...")
    # Get all the HEIC and MOV files in the directory
    heic_files = []
    mov_files = []

    for root, dirs, files in os.walk(DIR_PATH):
        for file in files:
            if file.endswith(".HEIC"):
                heic_files.append(os.path.join(root, file))
            elif file.endswith(".MOV"):
                mov_files.append(os.path.join(root, file))

    # Convert each HEIC file to JPEG

    print("Converting HEIC files to JPEG...")

    for heic_file in tqdm(heic_files):
        convert_heic_to_jpg(heic_file)

    # Convert each MOV file to MP4
    print("Converting MOV files to MP4...")

    for mov_file in tqdm(mov_files):
        convert_mov_to_mp4(mov_file)

if __name__ == "__main__":
    main()