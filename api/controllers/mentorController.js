var MongoClient = require('mongodb').MongoClient;
var url = "mongodb+srv://shafinsiddique:Ishafin98@cluster0-jrksj.mongodb.net/test?retryWrites=true&w=majority";

exports.getAllMentors = function (req, res) {
        MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("billiondollar");
        dbo.collection("mentors").find({}).toArray(function(err, result) {
          if (err) throw err;
          console.log(JSON.stringify(result));
          res.send(JSON.stringify(result));
          db.close();
        });
      });

}

