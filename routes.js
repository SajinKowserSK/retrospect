const path = require('path');
module.exports = function(app) {
    app.get('/', function(request, response) {
        response.render("index.ejs");
    })
}