module.exports = function(app) {
    var mentors = require("./controllers/mentorController");
    app.route('/mentors').get(mentors.getAllMentors);
}