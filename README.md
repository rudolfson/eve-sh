# eve-sh
EVE Online Shell

# Developer Notes
## Virtualenv
The project uses pipenv, I'm following instructions from
[The Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

## Libraries
* [Click](https://click.pocoo.org/) - command line parsing
* [click-shell](http://click-shell.readthedocs.io/) - turn click into a shell interpreter
* [Flask](http://flask.pocoo.org/) - http server 
* [Requests](http://docs.python-requests.org/en/master/) - http client
* [Maya](https://github.com/kennethreitz/maya) - date time library
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM and easy SQL

## Add a library
To add a new library during development use

    pipenv install <library>

## Run programm
You can install the program but need to configure the `setup.py` first. It
needs to include all the required libraries.

The run

    pipenv install -e .
    
to install the program in editable mode, i.e. it will use the local files.

To run the actual program just call it

    evesh <commands> <options>
