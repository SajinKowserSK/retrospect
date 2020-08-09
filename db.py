import pymongo
from pymongo import MongoClient
import bcrypt
from bson import ObjectId
from datetime import datetime
from pymongo import DESCENDING

client = pymongo.MongoClient("mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/<billiondollar>?retryWrites=true&w=majority")
main_db = client.get_database("billiondollar")


# save_room
# add_room_members
# get_room
# is_room_member
# get_room_members
# get_messages

mentors_collection = main_db.get_collection("mentors")
students_collection = main_db.get_collection("students")
rooms_collection = main_db.get_collection("rooms")
room_members_collection = main_db.get_collection("room_members")
messages_collection = main_db.get_collection("messages")


def save_room(room_name, created_by):
    room_id = rooms_collection.insert_one(
        {'name': room_name, 'created_by': created_by, 'created_at': datetime.now()}).inserted_id

    add_room_member(room_id, room_name, created_by, created_by, is_room_admin=True)
    return room_id

def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})

def add_room_members(room_id, room_name, usernames, added_by):
    room_members_collection.insert_many(
        [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
          'added_at': datetime.now(), 'is_room_admin': False} for username in usernames])

def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})

def is_room_member(room_id, username):
    return room_members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})

def get_room_members(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))

def save_message(room_id, text, sender):
    messages_collection.insert_one({'room_id':room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})

MESSAGE_FETCH_LIMIT = 5

def get_messages(room_id, page = 0):

    # how many msgs I want to skip before getting doc
    offset = page * MESSAGE_FETCH_LIMIT

    messages= list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(MESSAGE_FETCH_LIMIT).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H: %M")

    return messages[::-1]


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