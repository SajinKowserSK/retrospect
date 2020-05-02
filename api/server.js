var express = require('express');
var app = express();
var port = 3000;
var routes = require('./routes');
routes(app);
app.listen(port);
console.log('REST API listening for requests on port ' + port);
