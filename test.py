from db import *
import bcrypt
pwd = '1'
salt = bcrypt.gensalt()
hashedPassword = bcrypt.hashpw(pwd.encode('utf-8'), salt)
print(hashedPassword)


list1 = "https://www.linkedin.com/in/craigfmartin/?originalSubdomain=ca, https://www.linkedin.com/in/marcochchan/?originalSubdomain=ca, https://www.linkedin.com/in/khalil-kassam-a21a8471/?originalSubdomain=ca"
list1 = list1.split(",")
for link in list1:
    print(link)
print(list1[::-1])