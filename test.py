import requests

print(requests.get("https://barebilliondollar.herokuapp.com/" + "mentors/?email=sajinkowser@gmail.com").json()[0])