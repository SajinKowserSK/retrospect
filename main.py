import sys

from flask import Flask, render_template, request, session, redirect, url_for
import requests
app = Flask(__name__)
app.secret_key = "shafibullah"
api_base_url = "http://localhost:3000/"

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template("index.html", status=session['logged_in'])
    else:
        return render_template("mentors.html", status=session['logged_in'],
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

        tagColors = ['default', 'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light']

        if response.status_code == 200:
            session['logged_in'] = True

            return redirect(url_for('.profile', status=session['logged_in'], name=responseDict['name'], bio=responseDict['bio'], pic=responseDict['image'], keywords=responseDict['keywords'], tags = tagColors))

        elif response.status_code ==  404:

            return render_template("login.html", status=session['logged_in'], msgResponse = "User not found".upper())
        else:

            return render_template("login.html", status=session['logged_in'], msgResponse = "Email found but incorrect password".upper())

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("index.html", status=session['logged_in'])

@app.route("/profile")
def profile():
    return render_template("profile.html", status=request.args['status'], name=request.args['name'], bio=request.args['bio'], pic=request.args['pic'], keywords=request.args['keywords'], tags=request.args['tags'])
