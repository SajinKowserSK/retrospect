const MongoClient = require('mongodb').MongoClient;
const db_url = "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority";
const db_name = "billiondollar";
const collection_name = "mentors";
const querystring = require('querystring');

exports.getAllMentors = function (req, res) {
  MongoClient.connect(db_url, function (err, db) {
    if (err) throw err;
    var dbo = db.db(db_name);
    dbo.collection(collection_name).find({}).toArray(function (err, result) {
      if (err) throw err;
      res.send(JSON.stringify(result));
      db.close();
    });
  });
}

exports.findMentorsWithKeywords = function (req, res) {
  var keywords_from_query = req.query['keywords'].split(',');
  MongoClient.connect(db_url, function (err, db) {
    if (err) throw err;
    var dbo = db.db(db_name);
    dbo.collection(collection_name).find({ "keywords": { "$in":keywords_from_query} }).toArray(function (err, result) {
      if (err) throw err;
      res.send(JSON.stringify(result));
      db.close();
    });
  });

}

