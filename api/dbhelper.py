from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority")
database = client.get_database("billiondollar")


class StudentCollectionHelper:

    def __init__(self):
        self.collection = database.get_collection("students")

    def getStudents(self):
        students = []

        for docs in self.collection.find({}):
            del docs['_id']
            students.append(docs)

        return students


class MentorCollectionHelper:
    def __init__(self):
        self.collection = database.get_collection('mentors')


    def getMentors(self):
        mentors = []

        for docs in self.collection.find({}):
            del docs['_id']
            mentors.append(docs)

        return mentors

    def findMentorsWithKeywords(self, keywords):
        mentors = []

        for mentor in self.collection.find({"keywords":{"$in":keywords}}):
            del mentor['_id']
            mentors.append(mentor)

        return mentors

m = MentorCollectionHelper()
print(m.findMentorsWithKeywords(['Data Science']))