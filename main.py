import sys

from flask import Flask, render_template, request
import requests
app = Flask(__name__)
api_base_url = "http://localhost:3000/"

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
        print("hello sajin")
        return render_template("login.html")

    else:

        userEntry = {}
        userEntry["email"] = request.form['emailID']
        userEntry["password"] = request.form['passwordID']
        response = requests.post(api_base_url + "mentors", json=userEntry)

        if response.status_code == 200:

            return render_template("mentors.html")

        elif response.status_code ==  404:

            return render_template("login.html", msgResponse = "User not found".upper())
        else:

            return render_template("login.html", msgResponse = "Email found but incorrect password".upper())
