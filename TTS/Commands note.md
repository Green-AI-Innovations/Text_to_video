# Please note that the first step is building the application require docker to be installed and open, please follow link if you dont have it installed locally:
- https://docs.docker.com/desktop/install/windows-install/

# Please open docker and run the first command, make sure to open command promot in this folder and please note this may take up to 5 mins.
`Docker-compose build`

# The second command runs the built image from the previous step, make sure again to be in the same directory/folder
`Docker-compose up`

# How to generate voice ?
The docker container will turn on the software on port 8000 in whicch you can access /GenerateVoice endpoint that takes in text and returns the voice.
Endpoint (Post method) here - http://localhost:8000/GenerateVoice