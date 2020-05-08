const api_base_url = "https://barebilliondollar.herokuapp.com";
const https = require('https');

exports.get_home_page = function(request, response) {
    // handle what happens when we get a get request for the home page.
    response.render("index.ejs");
}

exports.get_login_page = function(request, response) {
    // handle what happens when we get a get request for the login page.
    response.render("login.ejs");
}

exports.post_home_page = function(request, response){ 
    var keywords = request.body.keywords;
    https.get(api_base_url + "/mentors/?keywords=" + keywords, (res) => {
        res.on('data', (data) => {
        response.render("mentors.ejs",{"mentors": JSON.parse(data), "keywords": keywords});
        })
    });

}

exports.post_login_page = function(request, response){
    var dict = [];
        dict.push({
            key: 'email',
            value: request.form['emailID']
        })

        dict.push({
            key: 'password',
            value: request.form['passwordID']
        })

        var APIresponse;

        APIresponse = request.post(
            api_base_url+'mentors',
            { json: dict },
        );

        var postResponse = APIresponse.json()
        var tagColors = tagColors = ['default', 'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light']

        if (response.statusCode == 200)
                response.render('profile.ejs', {"name": postResponse['name'], 'bio':postResponse['bio'], 'pic':postResponse['image'], 'keywords':postResponse['keywords'], 'tags': tagColors});

            else if (response.statusCode == 404)
                response.render("login.ejs", {"msgResponse":"USER NOT FOUND"});

            else
                response.render('login.ejs', {'msgResponse': "EMAIL FOUND BUT INCORRECT PASSWORD"});
}