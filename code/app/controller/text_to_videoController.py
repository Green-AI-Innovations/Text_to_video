import random
import string
import os
from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.lazykhschduler import scheduler
import json
import subprocess
import cv2


from services.gentelPhonemes import get_phonemes


router = APIRouter(
    responses={404: {"description": "Not found"}},

)


# Define the length of the random string
length = 12





@router.post('/textToVideo')
async def schedule_phonemes(transcript: UploadFile = File(...), sound: UploadFile = File(...),classfiedText: UploadFile = File(...) ):
# TODO check where each fie is saved
    randomeFilename=creat_randome_name()

    #  Read the transcript user inputed
    transcript = await transcript.read()
    transcript = transcript.decode('utf-8')
    transcript = removeTags(transcript)

    # get sound
    sound= await sound.read()

    # get phonemes
    phonemes = get_phonemes(transcript,sound,randomeFilename)

    # Call the scheduler 
    jsonFile= scheduler(transcript,phonemes,randomeFilename)
    

    # get classfied text TODO
    classfiedText = await classfiedText.read()
    classfiedText = classfiedText.decode('utf-8')
    with open(randomeFilename+'.txt', 'w') as file:
        file.write(classfiedText)


    # draw frames
    use_billboards=False
    jiggly_transitions=False
    draw_frames(randomeFilename,randomeFilename, use_billboards, jiggly_transitions)

    # finish the video and save it in the temprory folder
    keep_frames=False
    finsh_video(randomeFilename, keep_frames)


    # read video from file
    video = cv2.VideoCapture('temporary/'+randomeFilename +'_final.mp4')

    return  video


def draw_frames(file_name, use_billboards, jiggly_transitions):
    # input_file: scheduler csv and classfied emotion text should be the same name
    command = [
        "python3",
        "text_to_video/lazykh/videoDrawer.py",
        "--input_file",
        file_name,
        "--use_billboards",
        use_billboards,
        "--jiggly_transitions",
        jiggly_transitions,
    ]
    subprocess.run(command)

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


def finsh_video(input_file, keep_frames):
    command = [
        "python3",
        "text_to_video/lazykh/videoFinisher.py",
        "--input_file",
        input_file,
        "--keep_frames",
        keep_frames,
    ]
    subprocess.run(command)



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


def deleteAllFiles(folder):
 
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

    try:
        os.rmdir(folder)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (folder, e))
