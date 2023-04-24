# Pre-requites

The solutions requires creating an enviroment file, namely .env file which includes 2 variables the API azure TTS key and region. 
For example,
``
API_KEY=XXXXXXXXXXXX
REGION=westeurope
``
should be the content of the file. To get API key please log into your student I-Account in azure for students portal. Assuming you logged succssfully, under "RGR-InfolandProject02" resource you can find "ttst2v" instance of azure TTS that include 2 viable API keys that you replaces the xxxxxxxx placeholder with.

# Running the scripts (Commands)

0. `pip install python-dotenv` allow us to load environment variables to avoid commiting API keys in github repo. (for security purposed and best practises.)

1. `pip install azure-cognitiveservices-speech` which installs azure text-to-speech related libraries.

2. `python main.py` this essentially runs the python script locally and it generates an output audio file.

To control over what you would like to convert to speech you can adust the text present in ToConvert.txt file in the same directory.

