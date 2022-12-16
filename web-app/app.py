from flask import Flask, render_template, request, session, redirect, url_for, make_response, session, flash, Response
from dotenv import load_dotenv
from bson.json_util import dumps, loads, ObjectId
from mongodb import Database
from datetime import datetime
import bcrypt
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

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

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        elif  request.form.get('grey') == 'Grey':
            global grey
            grey=not grey
        elif  request.form.get('neg') == 'Negative':
            global neg
            neg=not neg
        elif  request.form.get('face') == 'Face Only':
            global face
            face=not face 
            if(face):
                time.sleep(4)   
        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

# camera

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
            return frame           

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    return frame

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            if(face):                
                frame= detect_face(frame)
            if(grey):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(neg):
                frame=cv2.bitwise_not(frame)    
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

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