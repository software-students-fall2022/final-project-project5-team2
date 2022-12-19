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

app.config['SESSION_TYPE'] = "mongodb"
app.config['SECRET_KEY'] = os.urandom(24)

#load config options from .env file
load_dotenv()

#connect to db
Database.initialize()
app.config['MONGO_dbname'] = 'users'

#routes
@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Home Page
    """
    # User logs out
    if request.method == "POST" and "username" in session:
        session.clear()

    if "username" in session:
        return redirect(url_for("feed"))

    return render_template('welcome.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    message = 'Please login to your account'
    if "username" in session:
        return redirect(url_for("feed"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_found = Database.find_single('users', {"username": username})
        if user_found:
            user_val = user_found['username']
            passwordcheck = user_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["username"] = user_val
                return redirect(url_for('feed'))
            else:
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Username not found'
            return render_template('login.html', message=message)
    return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        signup_user = Database.find_single('users', {'username': request.form['username']})
        if signup_user:
            flash(f"Username {request.form['username']} is already taken")
            return redirect(url_for('signup'))

        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        Database.insert_one('users', {'username': request.form['username'], 'password': hashed})
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route("/feed")
def feed():
    logged_in = "username" in session

    if logged_in:
        username = session['username']
    else:
        username = False
    
    sortby = request.args.get('sortby', '')
    query = request.args.get('query', '')
        
    posts = get_all_posts()

    posts = [post for post in posts if ( query.lower() in post['prompt'].lower())]
    now = datetime.now()
    for post in posts:
        date_posted = post['time_created']
        post['time_since'] = get_time_from(date_posted, now)
        post['votes'] = len(post['upvotes']) - len(post['downvotes'])
    posts = sort_posts(posts, sortby)
        
    return render_template("feed.html", posts=posts, logged_in=logged_in, username=username)

@app.route("/vote", methods=['POST'])
def vote():
    opposites = {
        'upvotes': 'downvotes',
        'downvotes': 'upvotes'
    }

    url = request.form.get('url', 'index')
    if "username" not in session:
        flash("You must sign in to vote")
        return redirect(url_for(url))
    
    username = session['username']
    
    post_id = ObjectId(request.form.get('post_id'))
    post = Database.find_single('photos', {"_id": post_id})
    vote = request.form.get('vote')

    op = opposites[vote]

    if username in post[vote]:
        Database.update('photos', {"_id": post_id}, {'$pull': { vote: username}})
        return redirect(url_for(url))
    
    if username in post[op]:
        Database.update('photos', {"_id": post_id}, {'$pull': { op: username}})

    Database.update('photos', {"_id": post_id}, {'$push': { vote: username}})
    
    return redirect(url_for(url))

@app.route("/post/<id>" ,methods=['POST', 'GET'])
def see_post(id):
    logged_in = "username" in session

    if logged_in:
        user = session["username"]
    else:
        user = ""

    if (request.method == "POST"):
        newCommentObj = {'username': user, 'comment': request.form['comment_body']}
        ## print(newCommentObj)
        id = ObjectId(id)
        Database.update('photos', {"_id": id}, {'$push': { 'comments' : newCommentObj} })

    id = ObjectId(id)
    post = Database.find_single('photos', {'_id': id})
    now = datetime.now()
    date_posted = post['time_created']
    post['time_since'] = get_time_from(date_posted, now)
    return render_template("post.html", post=post, logged_in=logged_in, username=user)


@app.route("/post/<id>", methods=['POST'])
def delete_post(id):
  if "username" not in session:
      return redirect(url_for("login"))
  else:
      user = session["username"]
  if (request.method == "POST"):
    id = ObjectId(id)

    post = Database.find_single('photos', {'_id': id})
    if post['username'] == user:
        Database.delete_one('photos', {'_id': id})

  return redirect(url_for("feed"))


@app.route("/new-post",methods=['POST', 'GET'])
def newPost():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        user = session["username"]

    if (request.method == "POST"):
        emptyArr = []
        newPostObj = {"username": user, 
        "photo": request.form.get('opImage'), 
        "prompt": request.form.get('opPrompt'),
        "time_created": datetime.now(),
        'comments': emptyArr,
        "downvotes": emptyArr,
        "upvotes": emptyArr,
        "votes": 0
        }
        Database.insert_one('photos', newPostObj)
        return redirect(url_for("feed"))

        
    else:
        return render_template("newPost.html", prompt=get_random_prompt(), user=user)

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
    prompt = random.choice(get_all_prompts())['message']
    return prompt


#run app
if __name__ == "__main__":


    PORT = os.getenv('PORT', 5001)
    HOST = os.getenv('HOST', '0.0.0.0')
    app.run(host=HOST, port=PORT)