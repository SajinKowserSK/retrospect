const api_base_url = "https://barebilliondollar.herokuapp.com/";
const https = require('https');

exports.get_home_page = function(request, response) {
    // handle what happens when we get a get request for the home page.
    response.render("index.ejs");
} 


exports.post_home_page = function(request, response){ 
    var keywords = request.body.keywords;
    console.log(api_base_url + "mentors/?keywords=" + keywords);
    https.get(api_base_url + "mentors/?keywords=" + keywords, (res) => {
        res.on('data', (data) => {
        response.render("mentors.ejs",{"mentors": JSON.parse(data), "keywords": keywords});
        })
    });
}