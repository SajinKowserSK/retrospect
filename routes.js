const path = require('path');
const https = require('https');

const api_base_url = "http://localhost:3000/";
module.exports = function(app) {
    
    app.get('/', function(request, response) {
        // handle what happens when we get a get request for the home page.
        response.render("index.ejs");
    })

    app.post('/', function(request, response) {
        // handle what happens when we get a post request from the home page.
        console.log("got post request");
        var keywords = request.body.keywords;
        console.log(api_base_url + "mentors/?keywords=" + keywords);
        https.get(api_base_url + "mentors/?keywords=" + keywords, (res) => {
        console.log('statusCode:', res.statusCode);
        console.log('headers:', res.headers);

        res.on('data', (d) => {
            process.stdout.write(d);
  });

})
    })
}
