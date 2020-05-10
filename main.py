import sys
import flask_login
from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user

app = Flask(__name__)
app.secret_key = "shafibullah"
api_base_url = "http://localhost:3000/"

login_manager = LoginManager()
login_manager.init_app(app)

# creates user class by inheriting default characteristics from flask user class
class User(UserMixin):

    def __init__(self, id, userInfo):
        self.id = id
        self.name = userInfo['name']
        self.bio = userInfo['bio']
        self.image = userInfo['image']
        self.keywords = userInfo['keywords']


@login_manager.user_loader
def load_user(user_id):
    return User.get_id()

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return render_template("mentors.html",
                               mentors=requests.get(api_base_url + "mentors/?keywords="+request.form['keywords']).json())


@app.route("/login", methods=['GET','POST'])
def login():


    if request.method == "GET":
        return render_template("login.html")


    else:


        userEntry = {}
        userEntry["email"] = request.form['emailID']
        userEntry["password"] = request.form['passwordID']
        response = requests.post(api_base_url + "mentors", json=userEntry)
        responseDict = response.json()

        user = User(1)
       # responseDict['name'], responseDict['bio'], responseDict['image'], responseDict['keywords'])

        tagColors = ['default', 'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light']

        if response.status_code == 200:
            login_user(user)

            flash('logged in success')

            return redirect(url_for('profile'))
            # return render_template("profile.html", )
            # return render_template("profile.html", name=user.id, bio=user.bio, image=user.image, keywords=user.keywords)

        elif response.status_code ==  404:

            return render_template("login.html", msgResponse = "User not found".upper())
        else:

            return render_template("login.html", msgResponse = "Email found but incorrect password".upper())

@app.route("/logout")
@login_required

def logout():
    logout_user()
    return redirect("/")

@app.route("/profile")

def profile():
    return render_template("profile.html",
                           name=request.args.get('name'), bio=request.args.get('bio'), image=request.args.get['image'], keywords=request.args.get('keywords'))
