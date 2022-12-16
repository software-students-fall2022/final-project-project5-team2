from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
from bson.json_util import dumps, loads, ObjectId
from mongodb import Database
from datetime import datetime

import random
import os

#instantiate the app
app = Flask(__name__)

#load config options from .env file
load_dotenv()

#connect to db
Database.initialize()

#routes
@app.route('/')

#home page
def home():
    """
    Home Page
    """
    return render_template('welcome.html')


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/feed")
def feed():
    posts = get_all_posts()
    sortby = request.args.get('sortby', '')
    posts = sort_posts(posts, sortby)
    now = datetime.now()
    for post in posts:
        date_posted = post['time_created']
        post['time_since'] = get_time_from(date_posted, now)
    return render_template("feed.html", posts=posts)

@app.route("/new-post")
def newPost():
    return render_template("newPost.html")

# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e):
    """
    Output errors.
    """
    print(e)
    return render_template('error.html', error=e), 404

def sort_posts(posts, sortby):
    if sortby == 'likes':
        param = 'votes'
    else:
        param = 'time_created'
    return sorted(posts, key=lambda x: x[param], reverse=True)

def get_time_from(date, now):
    difference = now - date
    days = difference.days
    years = days // 365
    months = days // 30
    weeks = days // 7
    seconds = difference.seconds
    minutes = seconds // 60
    hours = minutes // 60
    values = [years, months, weeks, days, hours, minutes, seconds]
    units = ['year', 'month', 'week', 'day', 'hour', 'minute', 'second']
    
    for i in range(len(values)):
        value = values[i]
        plural = ''
        if value > 0:
            unit = units[i]
            if value > 1:
                plural = 's'

            return f"{value} {unit}{plural} ago"
            
    return "0 seconds ago"

def get_all_posts():
    posts = Database.get_all('photos')
    return list(posts)

def get_all_prompts():
    prompts = Database.get_all('prompts')
    return loads(dumps(prompts))

def get_random_prompt():
    prompt = random.choice(get_all_prompts())
    return prompt

#run app
if __name__ == "__main__":
    PORT = os.getenv('PORT', 8080)
    app.run(port=PORT)