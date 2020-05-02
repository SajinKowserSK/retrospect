from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
api_base_url =
def home():
    if request.method == "GET":
        return render_template("index.html")

    return render_template("mentors.html", mentors=requests.get(""))

