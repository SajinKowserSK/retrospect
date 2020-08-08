import pymongo
from pymongo import MongoClient
import bcrypt

client = pymongo.MongoClient("mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/<billiondollar>?retryWrites=true&w=majority")
main_db = client.get_database("billiondollar")

mentors_collection = main_db.get_collection("mentors")

students_collection = main_db.get_collection("students")

def getUser(url):
    return mentors_collection.find_one({'url': url})


def updateName(email, new):
    foundUser = mentors_collection.find_one({'email': email})

    if foundUser:
        mentors_collection.update_one({'email': email}, {'$set': {'name': new}})


def updateHeader(email, new):
    foundUser = mentors_collection.find_one({'email': email})

    if foundUser:
        mentors_collection.update_one({'email': email}, {'$set': {'header': new}})

def updateEmail(email, new):
    foundUser = mentors_collection.find_one({'email': email})

    if foundUser:
        mentors_collection.update_one({'email': email}, {'$set': {'email': new}})

# STANDARDIZE HASHING IN SIGN UP PROCESS VS HERE
def updatePassword(email, new):
    return


    # foundUser = mentors_collection.find_one({'email': email})
    #
    # if foundUser:
    #     salt = bcrypt.gensalt()
    #     hashedPassword = bcrypt.hashpw(new.encode('utf-8'), salt)
    #     mentors_collection.update_one({'email': email}, {'$set': {'password': hashedPassword}})

def updateBio(email, new):
    foundUser = mentors_collection.find_one({'email': email})

    if foundUser:
        mentors_collection.update_one({'email': email}, {'$set': {'bio': new}})


def updateBio(email, new):
    foundUser = mentors_collection.find_one({'email': email})

    if foundUser:
        mentors_collection.update_one({'email': email}, {'$set': {'bio': new}})

def updateURL(email, new):
    foundUser = mentors_collection.find_one({'email': email})
    foundURL = mentors_collection.find_one({'url':new})

    if foundUser and not foundURL:
        mentors_collection.update_one({'email': email}, {'$set': {'url': new}})