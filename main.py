from flask import Flask, render_template, request, redirect, url_for, session
from db import *
import requests
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User
import re
from flask_socketio import SocketIO, join_room, leave_room

import bcrypt
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
app.secret_key = "shafibullah"
socketio = SocketIO(app)
app.run(debug=True)
api_base_url = "https://barebilliondollar.herokuapp.com/"

login_manager = LoginManager()
login_manager.init_app(app)


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])



@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

@login_manager.user_loader
def load_user(email):

    try:
        response = requests.get(api_base_url + "mentors/?email="+email).json()
        if len(response) > 0:
            return User(response[0])

    except:
        return redirect(home)

@app.route('/',methods=['GET'])
def home():
    if current_user.is_authenticated:
        print("user is already logged in")

    return render_template("index.html")
  

@app.route('/mentors',methods=['GET', 'POST'])
def mentors():
    if request.method == 'GET':
        return render_template("mentors.html")

    if request.method == 'POST':
        return render_template("mentors.html",
                                   mentors=requests.get(api_base_url +
                                   "mentors/?keywords="+request.form['keywords']).json(),
                                   keywords=request.form['keywords'])

@app.route("/login", methods=['GET','POST'])
def login():

    if request.method == 'POST':
        userEntry = {}
        userEntry["email"] = request.form['emailID']
        userEntry["password"] = request.form['passwordID']


        response = requests.post(api_base_url + "mentors", json=userEntry)
        tagColors = ['default', 'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light']
        if response.status_code == 200:
            user = User(response.json())
            user.authenticated = True
            login_user(user)
            session['logged_in'] = True
            print("logged in user")
            return redirect(url_for('profileRedirect'))

        elif response.status_code == 404:
            return render_template("login.html", msgResponse="User not found".upper())
        else:

            return render_template("login.html", msgResponse="Email found but incorrect password".upper())

    return render_template("login.html")
# @login_manager.user_loader
# def load_user(username):
#     return get_user(username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    print('logged out user')
    return redirect("/")


# PROBLEM
@app.route("/profile")
@login_required
def profileRedirect():
    return redirect(url_for('profile', url=current_user.URL))


# just check if username == current_user.email instead of makking a whole tmp user

@app.route("/profile/<url>")
def profile(url):
    tmpUser = getUser(url)

    if current_user.is_anonymous == False and current_user.URL == url:
        return render_template('profile.html')

    elif current_user.is_anonymous == True or current_user.URL != url:
        return render_template('view_profile.html', searched_user = tmpUser)

    else:
        return render_template("Error.html")


@app.route("/profile/editProfile", methods = ['GET', 'POST'])
@login_required
def editProfile():
    if request.method == 'GET':
        return render_template("editProfile.html")

    # make sure password is good

    else:

        userEntry = {}
        userEntry["email"] = current_user.email
        userEntry["password"] = request.form['currentPassword']
        response = requests.post(api_base_url + "mentors", json=userEntry)

        if response.status_code != 200:
            message = 'Incorrect Password'
            return render_template("editProfile.html", message=message)


        if request.form['updatePassword'] != request.form['confirmPassword']:
            message = 'Passwords do not match'
            return render_template("editProfile.html", message=message)


        email = current_user.email
        if request.form['name']:
            updateName(email, request.form['name'])


        if request.form['header']:
            updateHeader(email, request.form['header'])

        if request.form['email']:
            updateEmail(email, request.form['email'])


        if request.form['updatePassword']:

            if len(request.form['updatePassword']) >= 5 and re.match(r"^[A-Za-z]+\d\w*$", request.form['updatePassword']):
                updatePassword(email, request.form['updatePassword'])

            else:
                message = "Password does not meet requirements"
                return render_template("editProfile.html", message=message)

        if request.form['URL']:

            if mentors_collection.find_one({'url':request.form['URL']}):

                print(request.form['URL'])
                print(mentors_collection.find_one({'url':request.form['URL']}))
                message = "That URL is already in use. Please choose another."
                return render_template("editProfile.html", message=message)

            else:
                updateURL(email, request.form['URL'])

        if request.form['bio']:
            updateBio(email, request.form['bio'])

        return redirect(url_for('profileRedirect'))


# VERY IMPORTANT -- HVE TO MAKE SURE PROFILE URLS ARE UNIQUE
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('home'))

    message=''

    if request.method == 'POST':
        userEntry = {}
        userEntry["email"] = request.form['emailID']
        userEntry["password"] = request.form['passwordID']
        userEntry["name"] = request.form["name"]
        userEntry["keywords"] = request.form["keywords"].split(",")
        userEntry["bio"] = request.form["bio"]
        userEntry["image"] = "https://ibb.co/gF3MV75"
        userEntry["header"] = request.form["header"]
        userEntry["url"] = request.form["URL"]


        if mentors_collection.find_one({'url':request.form['URL']}):
            message = 'url already exists'
            return render_template('signup.html', msgResponse =message.upper())

        response = requests.post(api_base_url + "newmentor", json=userEntry)


        if response.status_code == 404:
            message= 'username already exists'
            return render_template("signup.html", msgResponse=message.upper())

        else:
            # saved user, redirecting to login page
            return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/pm/<mentor>', methods=['GET', 'POST'])
@login_required
def messages(mentor):
    roomName = "Private Chat"
    mentorAccount = getUser(mentor)

    members = sorted([current_user.URL, mentorAccount['url']])

    if check_room_exists(members):
        roomID = check_room_exists(members)['_id']

    else:
         roomID = save_room(roomName, current_user.URL, members)

    usernames = [mentorAccount['url']]
    return redirect(url_for('view_room', room_id = roomID))


@app.route('/messages/<room_id>', methods=['GET', 'POST'])
@login_required
def view_room(room_id):
    room = get_room(room_id)

    if room and is_room_member(room_id, current_user.URL):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)

        for x in range(0, len(room_members)):
            curr_url = room_members[x]

            curr = getUser(curr_url)['name']

            if curr != current_user.name:
                participant = curr

        # find other_participant object in room_members list (whether it be by name, url, etc.)
        # then pass as variable to jinja

        return render_template('view_room.html', username =current_user.name,
                               participant = participant,
                               room = room, room_members = room_members, messages = messages)

    else:
        return 'Room not found', 404


