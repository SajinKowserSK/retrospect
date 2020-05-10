var request = require('request');
module.exports = function(app) {

    var mentor_routes = require("./mentor_routes");
    app.route('/mentors').get(mentor_routes.getMentors);
    app.route('/mentors').post(mentor_routes.validate_mentor);


}
