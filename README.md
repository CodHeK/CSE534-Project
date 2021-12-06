# CSE 534: Final Project!

**Title:** Exploitation of Service Workers using Push Notifications


## File structure

    .
    ├── Chromium/src            # Instrumented browser code
    ├── collector               # Data collection module 
    ├── sw-adblock              # Dashboard to demo service worker based ad-blocker
    ├── requirements.txt
    └── README.md


## Run the code:

- Make sure you have docker installed on your desktop. If not go to https://docs.docker.com/get-docker/
- Clone this repository on your local machine.
	```
	$ git clone https://github.com/CodHeK/CSE534-Project.git
	```
- Create a virtual environment to install dependencies 
	```
	$ virtualenv venv
	$ . venv/bin/activate
	```
- Install all dependencies using `pip3`
	```
	$ pip3 install -r requirements.txt
	```
- Change directory to collector folder
	```
	$ cd collector
	```
- Update the website URL in `main.py` to the website you want to crawl and run:
	```
	$ python3 main.py
	```

- You can find the logged data and screenshots at `collector/containers_data/` as zipped files.


**Authors:**
Gauri Baraskar, Piyush Mital,  Gagan Ganapathy