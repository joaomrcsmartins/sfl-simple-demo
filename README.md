# SFL Simple Demo Application - Pet-A-Pet

Demo application that produces information-rich logs.
The goal is to extract information about those logs and apply an SFL technique to localize faults in the code.

The application is a simple service, Pet-A-Pet, composed of two services, Users and Pets.
The Users can request to pet a Pet, if they have enough snacks.
The Users can also request to buy more snacks.

## Requirements

* python - >= 3.10
* pipenv

## Usage

1. Setup environment: ```pipenv install```
2. Run load script in ```scripts/load_script.json``` by running ```pipenv run python main.py```
3. To send logs through MQ queue run ```pipenv run python logs_sender.py```
