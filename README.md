# MathsGPT Quickstart
This repository contains an example math tutor used in the OpenAI API quickstart tutorial. The app utilizes the Flask web framework.

## Setup
Follow the steps below to set up and run the MathsGPT app:

## Prerequisites
1. Python (if not already installed) Installation
2. Clone this repository to your local machine.

3. Navigate into the project directory:

 ```bash
$ cd mathsGPT
 ```
Create a new virtual environment:

 ```bash
$ python -m venv venv
$ . venv/bin/activate
 ```
Install the required dependencies:

 ```bash
$ pip install -r requirements.txt
 ```
 
## Configuration
Make a copy of the example environment variables file:

 ```bash
$ cp .env.example .env
 ```
Add your OpenAI API key to the newly created .env file.

Run the App
To start the app, execute the following command:

 ```bash
$ flask run
 ```
The app should now be accessible at http://localhost:5000 in your web browser.

Note: Ensure that the virtual environment is activated before running the app.

## Usage
Once the app is running, you can use it to ask for homework help by entering a problem within the textbox.

## License
This project is licensed under the MIT License. Feel free to modify and use it as per your requirements.

Please refer to the OpenAI API documentation for more details on how to integrate the OpenAI API into your projects.

If you encounter any issues or have any questions, please submit an issue on this repository.
