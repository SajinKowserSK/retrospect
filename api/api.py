from flask import Flask, request, jsonify
from dbhelper import MentorCollectionHelper
app = Flask(__name__)

mentorDB = MentorCollectionHelper()
@app.route('/',methods=['GET'])
def base():
    return 'home'

@app.route('/mentor/',methods=['GET'])
def findMentor():
    keywords = request.args.get('keywords').split()
    return jsonify(mentorDB.findMentorsWithKeywords(keywords))


