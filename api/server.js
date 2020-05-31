var express = require('express');
var app = express();
var port = process.env.PORT || 3000;
var routes = require('./routes');
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
routes(app);
app.listen(port);
console.log('REST API listening for requests on port ' + port);
