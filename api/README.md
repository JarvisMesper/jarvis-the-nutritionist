Flask API
=========

Flask API used by the bot.


## Installation

Create a virtual environment with Python 3.4 (or 3.5)

	virtualenv -p /usr/bin/python3.4 venv

Enter the virtual environment

	source venv/bin/activate

Install dependencies

	pip install --upgrade pip
	pip install -r requirements.txt

If your system says `_tkinter` is missing, you have to install it manually. For example on Ubuntu, simply type :

	sudo apt-get install python3-tk


## Usage

To launch the API

	python run.py

To exit the virtual environment

	deactivate
