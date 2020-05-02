from flask import Flask, render_template, request
import requests
app = Flask(__name__)
api_base_url = "http://127.0.0.1:5001/"

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return render_template("mentors.html",
                               mentors=requests.get(api_base_url + "mentor/?keywords="+request.form['keywords']).json())

