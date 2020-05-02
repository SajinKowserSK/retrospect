var MongoClient = require('mongodb').MongoClient;
var url = "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority";
var db_name = "billiondollar";
var collection_name = "mentors";

exports.getAllMentors = function (req, res) {
        MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db(db_name);
        dbo.collection(collection_name).find({}).toArray(function(err, result) {
          if (err) throw err;
          res.send(JSON.stringify(result));
          db.close();
        });
      });

}

