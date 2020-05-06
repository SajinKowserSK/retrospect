const path = require('path');
const requests = require('request');
const api_base_url = "http://localhost:3000/"
module.exports = function(app) {
    
    app.get('/', function(request, response) {
        // handle what happens when we get a get request for the home page.
        response.render("index.ejs");
    })

    app.post('/', function(request, response) {
        // handle what happens when we get a post request from the home page.
        console.log("got post request");
        var keywords = request.body.keywords;
        request.get(api_base_url + "mentors/?keywords=" + keywords, {"json":true}, function(err, res, body) {
            if (err) throw err;
            console.log(body.explanation);
        })
        
    })
}