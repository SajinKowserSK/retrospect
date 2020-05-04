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


@app.route("/login")
def login():
    return render_template("login.html")

