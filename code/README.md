# Wildradar Analyser and Manager

## Setup

<b>Prerequisites</b>

- Python

<details><summary><b>Setup locally</b></summary>

First create a secrets file called "appsettings.secrets.json" in the app>app>secrets folder.

Look at the [example.appsettings.secrets.json](./app/app/secrets/example.appsettings.secrets.json) file to see which secret variables are required.

To run the app open a new terminal and enter the following:
``` shell
# install dependencies
pip install -r requirements.txt

# go to app folder and run app in development
cd app
python -m uvicorn main:app --reload
```

</details>

<details><summary><b>Dokrize</b></summary>

ToDO

</details>

