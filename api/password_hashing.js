bcrypt = require('bcrypt');
const saltRounds = 10;

// check password entered by user, compare with password in database. If it matches, 
// respond with the users info, else respond with an error message.

exports.check_password = function(entered_password, user, response) {
    bcrypt.compare(entered_password, user['password'], function(err, result) {
        if (result == true) {
            response.status(200).send(JSON.stringify(user));
        }
        else {
            response.status(204).send(JSON.stringify({"error":"invalid password"}));
        }
    }) 

}

exports.generate_hash = function(password_string)  {
    const salt = bcrypt.genSaltSync(saltRounds);
    const hash = bcrypt.hashSync(password_string, salt);
    return hash
}




