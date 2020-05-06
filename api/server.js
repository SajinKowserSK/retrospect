var express = require('express');
var app = express();
var port = process.env.PORT || 3000;
var routes = require('./routes');

app.use(express.json());
app.use(express.urlencoded());
routes(app);
app.listen(port);
console.log('REST API listening for requests on port ' + port);
