import random
import string
import os
from fastapi import APIRouter
from fastapi import  File, UploadFile
from services.lazykhschduler import scheduler
import json
import subprocess
from services.lazykhVideoFinisher import Videofinisher
from services.gentelPhonemes import get_phonemes



router = APIRouter(
    responses={404: {"description": "Not found"}},

)


# Define the length of the random string
length = 12



def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper



@timer
@router.post('/textToVideo')
async def schedule_phonemes(transcript: UploadFile = File(...), sound: UploadFile = File(...),classfiedText: UploadFile = File(...) ):
# TODO check where each fie is saved
    randomeFilename=creat_randome_name()

    #  Read the transcript user inputed
    transcript = await transcript.read()
    transcript = transcript.decode('utf-8')
    transcript = removeTags(transcript)
    print('transcript')


    # get sound
    # Save audio file
    sound = await sound.read()
    path = "services/temporary/"
    save_audio(sound, path, randomeFilename)
    print('blah')


    # get phonemes
    phonemes = get_phonemes(sound,transcript,randomeFilename)
    print('phonemes')
    phonemes = json.dumps(phonemes)


    # Call the scheduler 
    jsonFile= scheduler(transcript,phonemes,randomeFilename)
    print('jsonFile')
    

    # get classfied text TODO
    classfiedText = await classfiedText.read()
    classfiedText = classfiedText.decode('utf-8')
    with open("services/temporary/"+randomeFilename+'.txt', 'w') as file:
        file.write(classfiedText)
    print('classfied text')

    # draw frames
    use_billboards="False"
    jiggly_transitions="False"
    draw_frames(randomeFilename, use_billboards, jiggly_transitions)
    print('draw frames')

    # finish the video and save it in the temprory folder


    
    # print('finshed video')

    audio_path = 'services/temporary/'+randomeFilename+'.wav'
    output_path = 'services/temporary/'+randomeFilename+'_final.mp4'
    frames_path=randomeFilename+'_frames'
    # create_video_with_audio(frames_path, audio_path, output_path)
    Videofinisher(frames_path,audio_path,output_path)
    print('created')

    # # Read the video file
    # video = cv2.VideoCapture(io.BytesIO(video_path))

    # # Create a response object
    # response = Response(content_type="multipart/x-mixed-replace; boundary=frame")

    # # Process the video frame by frame
    # while True:
    #     # Read a frame from the video
    #     ret, frame = video.read()

    #     if not ret:
    #         break

    #     # Convert the frame to JPEG format
    #     ret, buffer = cv2.imencode('.jpg', frame)
    #     frame = buffer.tobytes()

    #     # Add the frame to the response
    #     response.body = (
    #         b'--frame\r\n'
    #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    #     )

    #     # Yield the response to the client
    #     yield response
    # path='services/temporary/'
    # delete_files_with_prefix(path,randomeFilename)


def draw_frames(file_name, use_billboards, jiggly_transitions):
    command = [
        "python",
        "services/lazykhVideoDrawer.py",
        "--input_file",
        file_name,
        "--use_billboards",
        use_billboards,
        "--jiggly_transitions",
        jiggly_transitions,
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error drawer: {e}")

def creat_randome_name():
    while True:
        # Generate a random string of length 8
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        # Check if a file with that name already exists in the directory
        if not os.path.exists(random_string):
            break

    # Use the unique random string for the file name
    filename = random_string 

    return filename




def removeTags(script):
  TO_REMOVE = ["[","]","/"]

  newScript = script.replace("-"," ")
  for charToRemove in TO_REMOVE:
      newScript = newScript.replace(charToRemove,"")

  while "<" in newScript:
      start = newScript.index("<")
      end = newScript.index(">")+1
      newScript = newScript[:start]+newScript[end:]
  while "  " in newScript:
      newScript = newScript.replace("  "," ")
  while "\n " in newScript:
      newScript = newScript.replace("\n ","\n")
  while " \n" in newScript:
      newScript = newScript.replace(" \n","\n")
  while newScript[0] == " ":
      newScript = newScript[1:]

  return newScript


 
def delete_files_with_prefix(folder_path, prefix):
    """
    Deletes all files in a folder that start with a given prefix and end with either ".csv" or ".json".
    """
    for filename in os.listdir(folder_path):
        if filename.startswith("text_") or filename.startswith(prefix):
            os.remove(os.path.join(folder_path, filename))

import pydub

import wave

def save_audio(sound, path, name):
    # Open a new wave file with the specified parameters
    with wave.open(f"{path}{name}.wav", "wb") as output_file:
        output_file.setnchannels(1)  # Mono
        output_file.setsampwidth(2)  # 2 bytes per sample
        output_file.setframerate(44100)  # 44.1 kHz sample rate
        output_file.writeframes(sound)


import time

