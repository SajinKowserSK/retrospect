bcrypt = require('bcrypt');
const saltRounds = 10;
var myPlaintextPassword = "123456";

// check password entered by user, compare with password in database. If it matches, respond with the 
exports.check_password = function(entered_password, user, response) {
    bcrypt.compare(entered_password, user['password'], function(err, result) {
        if (result == true) {
            response.status(200).send(user);
        }
        else {
            response.status(404).send({"error":"invalid password"});
        }
    }) 

}

