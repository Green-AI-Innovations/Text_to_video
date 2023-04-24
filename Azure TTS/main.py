import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load the .env file
load_dotenv()

# Load API key and region from the .env file
api_key = os.getenv("API_KEY")
region = os.getenv("REGION")

# Configure the TTS client
speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

# Set the specific voice you want to use (replace with your desired voice)
voice = "en-US-JennyNeural"  # List can be found in link https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts#text-to-speech
speech_config.speech_synthesis_voice_name = voice

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Read the text from the file
with open("ToConvert.txt", "r") as file:
    text = file.read()

# Convert the text to SSML with the excited voice style
ssml = f"""
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='{voice}'>
    <prosody rate='1.0' pitch='+5%' volume='100%'>
      <mstts:express-as style='cheerful'>
        {text}
      </mstts:express-as>
    </prosody>
  </voice>
</speak>
"""

# Convert SSML to speech and save to a file
output_file_path = "output_audio_with_excited_voice.wav"
speech_result = speech_synthesizer.speak_ssml_async(ssml).get()
if speech_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    with open(output_file_path, "wb") as audio_file:
        audio_file.write(speech_result.audio_data)
    print(f"Speech synthesized with excited voice '{voice}' and saved to {output_file_path}")
else:
    print(f"Speech synthesis failed with status: {speech_result.reason}")