# Todo API

Backend for todo API. Requires env file with configurations according to _.env.sample_ file to run.

## Stack

- Python 3.8
- Flask-restful
- Flask-jwt-extended
- Flask-SQLAlchemy
- SQLite local db

## Install dependencies

Configure virtual env:

`$ pip install virtualenv`

in project root:

`$ virtualenv venv`

`$ source venv/bin/activate`

install dependencies:

`$ pip install -r requirements.txt`

## Run project in simulator

After having configured `local.env` file according to .env.sample, run:

`$ export ENVIRONMENT=local`

`$ python app.py`
