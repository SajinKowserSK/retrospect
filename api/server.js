var express = require('express');
var app = express();
var port = 3000;
var routes = require('./routes');
var bodyParser = require('body-parser');
routes(app);
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json())
app.listen(port);
console.log('REST API listening for requests on port ' + port);
