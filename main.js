const express = require('express');
const routes = require('./routes');
const app = express();
var port = 5000;
app.set('views','./views');
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/static'));
routes(app); // create routes for the website.
app.listen(port);
console.log('Web server running on port ' + port);
