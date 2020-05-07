const path = require('path');
const handler = require('./route_handlers');

module.exports = function(app) {
    app.get('/', handler.get_home_page);
    app.post('/', handler.post_home_page);

      // for get request of log in page
    app.get('/login', handler.get_login_page);

    // for post request of log in page
    app.post('login', handler.post_login_page);


}

