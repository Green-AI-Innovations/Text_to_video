import subprocess

def video_finisher(input_file, keep_frames):
    command = [
        "python3",
        "text_to_video/lazykh/videoFinisher.py",
        "--input_file",
        input_file,
        "--keep_frames",
        keep_frames,
    ]
    subprocess.run(command)