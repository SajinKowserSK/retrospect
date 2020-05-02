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
    mentors_search = jsonify(mentorDB.findMentorsWithKeywords(keywords))
    print(type(mentors_search))
    return mentors_search


