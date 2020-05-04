const MongoClient = require('mongodb').MongoClient;
const db_url = "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority";
const db_name = "billiondollar";
const collection_name = "mentors";
const querystring = require('querystring');

function getMentorsWithKeywords(database, req, res) {
  keywords = req.query['keywords'].split(',').map(keyword_string => keyword_string.trim());
  database.collection(collection_name).find({ "keywords": { "$all": keywords } }).toArray(function (err, result) {
    if (err) throw err;
    res.send(JSON.stringify(result));
  });

}

function getMentorWithEmail(database, req, res) {
  database.collection(collection_name).find({"email":req.query['email']}).toArray(function (err, result) {
    if (err) throw err;
    res.send(JSON.stringify(result));
  }) 
    
}


function getAllMentors(database, req, res) {
  database.collection(collection_name).find({}).toArray(function (err, result) {
    if (err) throw err;
    res.send(JSON.stringify(result));
  });
}


exports.getMentors = function (req, res) {
  MongoClient.connect(db_url, function (err, db) {
    if (err) throw err;
    var dbo = db.db(db_name);
    if ('keywords' in req.query) {
      getMentorsWithKeywords(dbo, req, res);
    }

    else if ('email' in req.query){ 
      getMentorWithEmail(dbo, req, res);
    }

    else {
      getAllMentors(dbo, req, res);
    }
    db.close();
  });
}


