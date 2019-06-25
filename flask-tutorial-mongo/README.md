# Flask Tutorial
- http://flask.pocoo.org/docs/1.0/tutorial/

## Description
- This is a modified version of the linked tutorial to work with mongoDB
- Here, mongoEngine is used to define schema for database
- MongoEngine is like ORM but for non-relational

## Setup the virtual environment
```Console
$ python -m venv venv
$ source venv/Scripts/activate
```


## Run in Development Mode
```Console
$ pip install -e .
$ pip list
[ view flaskr in your current working directory ]

$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```


## Run in Test Mode
```Console
$ pip install '.[test]'
$ which pytest
[ view where pytest is running from ... makes sense?]
$ pytest
[ view testing overview with coverage]
$ pytest --verbose
[ view detailed testing overview]
```

## Refresh the database
```console
$ flask init-db
```