module.exports = function(app) {
    var mentorsCollection = require("./mentorCollectionHelper");
    app.route('/mentors').get(mentorsCollection.getAllMentors);
}