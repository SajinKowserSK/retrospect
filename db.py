from pymongo import MongoClient

client = MongoClient("mongodb+srv://adminUser:<password>@chatapp-ubwoq.mongodb.net/<dbname>?retryWrites=true&w=majority")
main_db = client.get_database("billiondollar")

mentors_collection = main_db.get_collection("mentors")

students_collection = main_db.get_collection("students")

def updateName(email, new):
    return

def updateHeader(email, new):
    return

def updateEmail(email, new):
    return

def updatePassword(email, new):
    return

def updateBio(email, new):
    return