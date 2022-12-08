from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os

import pymongo

#instantiate the app
app = Flask(__name__)

#load config options from .env file
load_dotenv()

#connect to db


#routes
@app.route('/')

#home page
def home():
    """
    Home Page
    """
    return render_template('base.html')

# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e):
    """
    Output errors.
    """
    return render_template('error.html', error=e), 404

#run app
if __name__ == "__main__":
    PORT = os.getenv('PORT',5000)
    app.run(port=PORT)