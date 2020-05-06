const express = require('express');
const routes = require('./routes');
const app = express();
var port = 5000;
app.set('views','./views');
app.set('view engine', 'ejs');

app.use(express.static(__dirname + '/static')); // set static folder to ./static.

app.use(express.urlencoded()); // Parse URL-encoded bodies (as sent by HTML forms)

app.use(express.json()); // Parse JSON bodies (as sent by API clients)

routes(app); // create routes for the website, see routes.js file.

app.listen(port);
console.log('Web server running on port ' + port);


