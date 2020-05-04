const MongoClient = require('mongodb').MongoClient;
const db_url = "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority";
const db_name = "billiondollar";
const collection_name = "mentors";
const querystring = require('querystring');

function searchMentorsCollectionAndSendResponse(database, response, query_dict) {
  database.collection(collection_name).find(query_dict).toArray(function (err, result) {
    if (err) throw err;
    response.send(JSON.stringify(result));
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
