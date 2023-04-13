import cv2
import os
import argparse
import os.path
import os
import subprocess
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip


def Videofinisher(image_folder, audio_path, video_name):



    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()


  # Add audio to video
    video_clip = VideoFileClip(video_name)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(video_name.replace(".mp4", "_with_audio.mp4"), codec="mpeg4")



# def fisher(INPUT_FILE,KEEP_FRAMES):
#     ffmpeg='ffmpeg'

#     command = ffmpeg+" -r 30 -f image2 -s 1920x1080 -i "+INPUT_FILE+"_frames/f%06d.png -i "+"services/temporary/"+INPUT_FILE+".wav -vcodec libx264 -b 4M -c:a aac -strict -2 "+INPUT_FILE+"_final.mp4 "
#     subprocess.call(command, shell=True)

#     if KEEP_FRAMES == "F":
#         emptyFolder(INPUT_FILE+"_frames")
