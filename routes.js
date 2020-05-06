const path = require('path');
const handler = require('./route_handlers');

module.exports = function(app) {
    app.get('/', handler.get_home_page);
    app.post('/', handler.post_home_page);
}

