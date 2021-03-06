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
waitlist_collection = main_db.get_collection("waitlist")


def resetRooms():
    messages_collection.delete_many({})
    rooms_collection.delete_many({})
    print("Done, Reset all rooms and messages")

def check_room_exists(members):
    return rooms_collection.find_one({"members":members})

def save_room(room_name, created_by, members, latest):
    # [ {
    #    "shafin": {"read": False, "lastJoined": datetime, "lastLeft": datetime},
    #    "sajin": {"read": False, "lastJoined": datetime, "lastLeft": datetime}
    #
    #    } ]

    roomLog = [{}]

# come back

    for member in members:
        activity = roomLog[0]
        # input key for member
        activity[member] = {}

        # create keys for members dict
        activity[member]["read"] = False
        activity[member]["lastJoined"] = None
        activity[member]["lastLeft"] = None

    room_id = rooms_collection.insert_one(
        {'name': room_name, 'created_by': created_by, 'members': members,
         'created_at': datetime.now(), 'latest':latest, "roomLog": roomLog}).inserted_id

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
    members = rooms_collection.find_one({'_id': ObjectId(room_id)})
    members = members['members']
    for member in members:
        if username == member:
            return True

    return False

def get_room_members(room_id):
    #return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))
    members = rooms_collection.find_one({'_id': ObjectId(room_id)})

    members = members['members']
    return members

def save_message(room_id, text, sender, sender_name):
    messages_collection.insert_one({'room_id':room_id, 'text': text,
                                    'sender': sender, 'created_at': datetime.now(),
                                    'senderName': sender_name})
MESSAGE_FETCH_LIMIT = 100

def get_messages(room_id, page = 0):

    # how many msgs I want to skip before getting doc
    offset = page * MESSAGE_FETCH_LIMIT

    messages= list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(MESSAGE_FETCH_LIMIT).skip(offset))
    # for message in messages:
    #     message['created_at'] = message['created_at'].strftime("%d %b, %H: %M")

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


def getRoomLog(roomID):
    room = get_room(roomID)

    if room is None:
        return None

    return room['roomLog']

def getUserLastJoin(roomID, userURL):
    roomLog = getRoomLog(roomID)[0]
    userActivity = roomLog[userURL]
    return userActivity["lastJoined"]

def getUserLastLeft(roomID, userURL):
    roomLog = getRoomLog(roomID)[0]
    userActivity = roomLog[userURL]
    return userActivity["lastLeft"]

def updateLastJoin(roomID, userURL):

    updated = []
    roomLog = getRoomLog(roomID)[0]
    userActivity = roomLog[userURL]
    userActivity["lastJoined"] = datetime.now()
    userActivity["read"] = True
    roomLog[userURL] = userActivity
    updated.append(roomLog)

    rooms_collection.update_one({'_id': ObjectId(roomID)}, {'$set': {"roomLog": updated }})

def updateLastLeft(roomID, userURL):
    updated = []
    roomLog = getRoomLog(roomID)[0]
    userActivity = roomLog[userURL]
    userActivity["lastLeft"] = datetime.now()
    roomLog[userURL] = userActivity
    updated.append(roomLog)

    rooms_collection.update_one({'_id': ObjectId(roomID)}, {'$set': {"roomLog": updated}})

def userRead(roomID, userURL, bool):
    updated = []
    roomLog = getRoomLog(roomID)[0]
    userActivity = roomLog[userURL]
    userActivity["read"] = bool
    roomLog[userURL] = userActivity
    updated.append(roomLog)

    rooms_collection.update_one({'_id': ObjectId(roomID)}, {'$set': {"roomLog": updated}})

def check_unread_messages(roomID, userURL):
    messages = get_messages(roomID)[::-1]
    for message in messages:
        lastLeft = getUserLastLeft(roomID, userURL)
        if message['sender'] != userURL and lastLeft is None or lastLeft is not None and lastLeft < message['created_at']:
            userRead(roomID, userURL, False)


def update_room_status_for_user(userURL):
    # need to find all the rooms where userURL is a member
    user_rooms = list(rooms_collection.find({"members": { "$all": [userURL]}}))
    for room in user_rooms:
        check_unread_messages(str(room['_id']), userURL)

def check_participant_received(room_id, user_url):
    curr_room = rooms_collection.find_one({'_id': ObjectId(room_id)})['members']
    participant_url = user_url
    for member in curr_room:
        if member != user_url:
            participant_url = member

    check_unread_messages(room_id, participant_url)

def update_latest(roomID):
    rooms_collection.update_one({'_id': ObjectId(roomID)}, {'$set': {"latest": datetime.now()}})

def get_recent_messages(userURL):
    user_rooms = list(rooms_collection.find({"members": {"$all": [userURL]}}))
    sorted_user_rooms = sorted(user_rooms, key=lambda x: x['latest'], reverse=True)
    return sorted_user_rooms

def get_name(userURL):
    return mentors_collection.find_one({"url": userURL})['name']

def get_image(userURL):
    return mentors_collection.find_one({"url": userURL})['image']

def get_most_recent_message(roomID):
    msgs = get_messages(str(roomID))

    if msgs is not None and len(msgs) > 0:

        msgs = msgs[-1]
        return msgs['text']

    else:
        return "Start the conversation!"

def format_time(time):
    return time.strftime("%I:%M %p")


def is_unread(room_id, user_url):
    # get room log for room_id
    # check if room_log[0][user_url]['read'] == True, if yes return True else return False
    room_id = str(room_id)
    curr_room = rooms_collection.find_one({'_id': ObjectId(room_id)})['roomLog'][0]
    if curr_room and curr_room[user_url]['read'] != True:
        return True

    return False


def add_to_signup(email, type):
    waitlist_collection.insert_one({"email":email, "type":type})