""" File to run the App to put up the project. """
from project import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)