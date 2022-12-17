from flask import Flask, render_template, request, session, redirect, url_for, make_response, session, flash, Response
from dotenv import load_dotenv
from bson.json_util import dumps, loads, ObjectId
from mongodb import Database
from datetime import datetime
import bcrypt


import random
import os

#instantiate the app
app = Flask(__name__)

#load config options from .env file
load_dotenv()

#connect to db
Database.initialize()
app.config['MONGO_dbname'] = 'users'
#routes
@app.route('/')

#home page
def index():
    """
    Home Page
    """
    return render_template('welcome.html')

@app.route("/login")
def login():
    # message = 'Please login to your account'
    # if "email" in session:
    #     return redirect(url_for("logged_in"))

    # if request.method == "POST":
    #     email = request.form.get("email")
    #     password = request.form.get("password")

       
    #     email_found = records.find_one({"email": email})
    #     if email_found:
    #         email_val = email_found['email']
    #         passwordcheck = email_found['password']
            
    #         if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
    #             session["email"] = email_val
    #             return redirect(url_for('logged_in'))
    #         else:
    #             if "email" in session:
    #                 return redirect(url_for("logged_in"))
    #             message = 'Wrong password'
    #             return render_template('login.html', message=message)
    #     else:
    #         message = 'Email not found'
    #         return render_template('login.html', message=message)
    return render_template("login.html")

@app.route("/signup")
def signup():
    # if request.method == 'POST':
    #     users = mongo.db.users
    #     signup_user = users.find_one({'username': request.form['username']})

    # if signup:
    #     flash(request.form['username'] + ' username is already exist')
    #     return redirect(url_for('signup'))

    # hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
    # users.insert({'username': request.form['username'], 'password': hashed})
    # return redirect(url_for('login'))

    return render_template("signup.html")

@app.route("/feed")
def feed():
    if "email" in session:
        email = session["email"]
            
        posts = get_all_posts()
        sortby = request.args.get('sortby', '')
        posts = sort_posts(posts, sortby)
        now = datetime.now()
        for post in posts:
            date_posted = post['time_created']
            post['time_since'] = get_time_from(date_posted, now)
    else:
        return redirect(url_for("login"))
    return render_template("feed.html", posts=posts)

@app.route("/post/<id>")
def see_post(id):
    post = Database.find_single('photos', id, "_id")
    print(post)
    return render_template("post.html", post=post)



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


# auth

# @app.route("/", methods=['post', 'get'])
# def index():
#     # message = ''
#     # if 'email' in session:
#     #     return redirect(url_for("logged_in"))
#     # if request.method == "POST":
#     #     user = request.form.get("user")
#     #     email = request.form.get("email")

#     #     password = request.form.get("password")
#     #     password_confirm = request.form.get("password_confirm")

#     #     user_found = records.find_one({"user": user})
#     #     email_found = records.find_one({"email": email})

#     #     if user_found:
#     #         message = "This username is already taken."
#     #         return render_template('index.html')
#     #     if email_found:
#     #         message = "This email already has an account linked to it."
#     #         return render_template('index.html')
#     #     if password != password_confirm: 
#     #         message = "Passwords should match."
#     #         return render_template('index.html')
#     #     else:
#     #         hashed = bcrypt.hashpw(password_confirm.encode('utf-8'), bcrypt.gensalt())
#     #         user_input = {"user": user, 'email': email, 'password': hashed}
#     #         records.insert_one(user_input)

#     #         user_data = records.find_one({"email": email})
#     #         new_email = user_data['email']

#     #         return render_template('feed.html', email = new_email)
#     return render_template('index.html')


#run app
if __name__ == "__main__":
    PORT = os.getenv('PORT', 8080)
    app.run(port=PORT)