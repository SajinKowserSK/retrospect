from flask import Flask, render_template, request, redirect, url_for, session
from db import *
import requests
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User
import re
import bcrypt
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
app.secret_key = "shafibullah"
app.run(debug=True)
api_base_url = "https://barebilliondollar.herokuapp.com/"

# MONGO STUFF



login_manager = LoginManager()
login_manager.init_app(app)

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
  

@app.route('/mentors',methods=['POST'])
def mentors():
    return render_template("mentors.html",
                               mentors=requests.get(api_base_url + "mentors/?keywords="+request.form['keywords']).json(), keywords=request.form['keywords'])

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
    return redirect(url_for('profile', username=current_user.email))


# just check if username == current_user.email instead of makking a whole tmp user

@app.route("/profile/<username>")
def profile(username):
    tmpUser = getUser(username)

    if tmpUser is None:
        return render_template('Error.html')

    elif current_user is not None and tmpUser != current_user:
        return render_template('view_profile.html', searched_user = tmpUser)

    elif tmpUser is not None and current_user is not None and tmpUser == current_user:
        return render_template('profile.html')

    else:
        return render_template("Error.html")


@app.route("/editProfile", methods = ['GET', 'POST'])
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



        if request.form['bio']:
            updateBio(email, request.form['bio'])

        return redirect(url_for('profileRedirect'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('home'))

    message=''

    if request.method == 'POST':
        userEntry = {}
        userEntry["email"] = request.form['emailID']
        userEntry["password"] = request.form['passwordID']
        userEntry["name"] = ""
        userEntry["keywords"] = []
        userEntry["bio"] = ""
        userEntry["image"] = "https://ibb.co/gF3MV75"
        userEntry["header"] = ""


        response = requests.post(api_base_url + "newmentor", json=userEntry)


        if response.status_code == 404:
            message= 'username already exists'
            return render_template("signup.html", msgResponse=message.upper())

        else:
            # saved user, redirecting to login page
            return redirect(url_for('login'))

    return render_template('signup.html')
