#  This class will take transcript and  audio and return the phonemes
from flask import Flask, request
import requests
from pydub import AudioSegment
import os





def get_phonemes(mp3_audio, text_file):
    # Set the URL for the external API
    url = 'http://localhost:8765/transcriptions?async=false'

    # Set the files and data for the HTTP POST request
    files = {'audio': (mp3_audio.filename, mp3_audio.stream),
             'transcript': (text_file.filename, text_file.stream)}


    # Send the HTTP POST request to the external API
    response = requests.post(url, files=files)

    # Save the response to a file
    # with open('temporary/phonemes.txt', 'rw') as f:
    #     f.write(response.text)

    # Return the response from the external API
    return response.text

