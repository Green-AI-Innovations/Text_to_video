#  This class will process the tect and call other classes then return the result(Video)
from flask import Flask, request
import requests
from pydub import AudioSegment
import os


def create_video_from_text(transcript: str):

    print(transcript)
    directory = 'temporary'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('temporary/transcript.txt', 'w') as text_file:
        # Write the text to the file
        text_file.write(transcript)

    # get audio
    audio = convert_text_to_speach(transcript)
    # Get phonemes
    phonemes = get_phonemes()

    # TODO pass transcript and audio and phonemes to lazykh


    return transcript


def get_phonemes():
    # Set the URL for the external API
    url = 'http://localhost:8765/transcriptions?async=false'

    # Set the files and data for the HTTP POST request
    files = {'audio': ('example.mp3', open('temporary/example.mp3', 'rb')),
             'transcript': ('example.txt', open('temporary/example.txt', 'rb'))}

    # Send the HTTP POST request to the external API
    response = requests.post(url, files=files)

    # Save the response to a file
    with open('temporary/phonemes.txt', 'rw') as f:
        f.write(response.text)

    # Return the response from the external API
    return response.text


def convert_text_to_speach(transcript: str):

    # this is an example of audio file later we will use Amazon poly TODO
    # load the audio file using the path
    audio_file = AudioSegment.from_file('temporary/example.mp3', format='mp3')


    # after geting the audio from Amason poly we save it temporarly
    audio_file.export('temporary/example.mp3', format='mp3')

    # Get the audio data //No need maybe future use
    # return audio_file.raw_data


def lazykh(transcript: str,audio:AudioSegment,phonemes:str):
# TODO
    return 0