const MongoClient = require('mongodb').MongoClient;
const db_url = "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority";
const db_name = "billiondollar";
const collection_name = "mentors";
const querystring = require('querystring');
const password = require('./password_hashing');
function searchMentorsCollectionAndSendResponse(database, response, query_dict) {
  database.collection(collection_name).find(query_dict).toArray(function (err, result) {
    if (err) throw err;
    response.send(JSON.stringify(result));
  });
}

exports.validate_mentor = function(req, res) {
  MongoClient.connect(db_url, function (err, db) {
    if (err) throw err;
    var dbo = db.db(db_name);
    dbo.collection(collection_name).find({"email":req.body.email}).toArray(function (err, result) {
      if (err) throw err;
      if (result.length > 0) {
        password.check_password(req.body.password, result, res);
      }
      else {
        res.status(404).send({"error":"user does not exist"});
      }
    });
    db.close();
  });

}
exports.getMentors = function (req, res) {
  MongoClient.connect(db_url, function (err, db) {
    if (err) throw err;
    var dbo = db.db(db_name);
    var query_dict =  {}
    if ('keywords' in req.query) {
      keywords = req.query['keywords'].split(',').map(keyword_string => keyword_string.trim());
      query_dict = { "keywords": { "$all": keywords }};
    }

    else if ('email' in req.query){ 
      query_dict = {"email":req.query['email']}
    }

    searchMentorsCollectionAndSendResponse(dbo, res, query_dict);
    db.close();
  });
}


