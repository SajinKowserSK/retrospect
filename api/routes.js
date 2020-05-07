module.exports = function(app) {
    var mentor_routes = require("./mentor_routes");

    // search landing page
    app.route('/mentors').get(mentor_routes.getMentors);

    // search function using the form
    app.route('/mentors').post(mentor_routes.validate_mentor);

    // for get request of log in page
    app.get('/login', function(req, res) {  res.render('login');});



}
