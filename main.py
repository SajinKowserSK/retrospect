from flask import Flask, render_template, request, redirect, url_for, session
import requests
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User
import bcrypt

app = Flask(__name__)
app.secret_key = "shafibullah"
app.run(debug=True)
api_base_url = "https://barebilliondollar.herokuapp.com/"

# MONGO STUFF






login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    return User(requests.get(api_base_url + "mentors/?email="+email).json()[0])

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
    if request.method == "GET":
        return render_template("login.html")

    else:
        userEntry = {}
        userEntry["email"] = request.form['emailID']
        userEntry["password"] = request.form['passwordID']

        # make request to API
        response = requests.post(api_base_url + "mentors", json=userEntry)
        tagColors = ['default', 'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light']


        if response.status_code == 200:
            user = User(response.json())
            user.authenticated = True
            login_user(user, remember=True)
            print("logged in user")
            return redirect(url_for('profile'))

        elif response.status_code == 404:
            return render_template("login.html", msgResponse="User not found".upper())
        else:

            return render_template("login.html", msgResponse="Email found but incorrect password".upper())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    print('logged out user')
    return redirect("/")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/register',methods=['GET'])
def register():
    # if request.method == 'POST':
    #     users = mongo.db.users
    #     existing_user = users.find_one({'name':request.form['username']})
    #
    #     if existing_user is None:
    #         hashedPassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
    #         users.insert({'name' : request.form['username'], 'password': hashedPassword})
    #         session['username'] = request.form['username']
    #         return redirect(url_for('index'))
    #
    #     # can be passed as a variable to sign up html page
    #     return 'username already exists'
    #
    # else:
    return render_template("signup.html")