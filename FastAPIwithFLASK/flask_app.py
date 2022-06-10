# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask

# Flask constructor takes the name of 
# current module (__name__) as argument.
flask_app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call 
# the associated function.
@flask_app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World, This is Flask API'


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    flask_app.run(port=3000)
