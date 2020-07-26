import pymongo
from pymongo import mongo_client


client = pymongo.MongoClient("mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/<billiondollar>?retryWrites=true&w=majority")
db = client.test

main_db = client.get_database("billiondollar")

mentors_collection = main_db.get_collection("mentors")

students_collection = main_db.get_collection("students")

def updateName(email, new):
    foundUser = mentors_collection.find_one({'email': email})

    if foundUser:
        mentors_collection.update_one({'email': email}, {'$set': {'name': new}})


updateName('sajinkowser@gmail.com', 'sajinv2')