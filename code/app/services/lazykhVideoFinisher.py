import argparse
import os.path
import os
import subprocess

def emptyFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    try:
        os.rmdir(folder)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (folder, e))


parser = argparse.ArgumentParser(description='blah')
parser.add_argument('--input_file', type=str,  help='the script')
parser.add_argument('--keep_frames', type=str,  help='do you want to keep the thousands of frame still images, or delete them?')
args = parser.parse_args()
INPUT_FILE = args.input_file
KEEP_FRAMES = args.keep_frames



# command = "ffmpeg -r 30 -f image2 -s 1920x1080 -i "+INPUT_FILE+"_frames/f%06d.png -i "+"services/temporary/"+INPUT_FILE+".wav -vcodec libx264 -b 4M -c:a aac -strict -2 "+INPUT_FILE+"_final.mp4 "
# subprocess.call(command, shell=True)

import av
import os

# Set up input file paths
input_images_path = INPUT_FILE + '_frames'
input_audio_path = 'services/temporary/' + INPUT_FILE + '.wav'
num_frames=len(os.listdir(input_images_path))


# Set up output file path
output_video_path = 'services/temporary/'+INPUT_FILE + '_final.mp4'

# Set up video encoder
# Set up video encoder
container = av.open(output_video_path, mode='r')
video_stream = container.streams.video[0]

# Set up audio encoder
audio_stream = container.streams.audio[0]

# Set up output file path
output_video_path = INPUT_FILE + '_final.mp4'

# Set up video encoder
container = av.open(output_video_path, mode='w')
video_stream_out = container.add_stream('libx264', rate=30)
video_stream_out.width = 1920
video_stream_out.height = 1080
video_stream_out.pix_fmt = 'yuv420p'
video_stream_out.bit_rate = 4000000

# Set up audio encoder
audio_stream_out = container.add_stream('aac')
audio_stream_out.bit_rate = 256000

# Encode video frames
for packet in container.demux(video_stream):
    for frame in packet.decode():
        frame = frame.reformat(width=video_stream_out.width, height=video_stream_out.height, format='yuv420p')
        frame = frame.to_rgb().to_ndarray()
        packet_out = video_stream_out.encode(frame)
        container.mux(packet_out)

# Encode audio and write it to the output container
audio = av.open(input_audio_path)
for packet in audio_stream_out.encode(audio.decode(audio_stream)):
    container.mux(packet)

# Close the output container to finalize the output file
container.close()

if KEEP_FRAMES == "F":
    emptyFolder(INPUT_FILE+"_frames")
