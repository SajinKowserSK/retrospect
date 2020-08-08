import bcrypt
pwd = '12345'
salt = bcrypt.gensalt()
hashedPassword = bcrypt.hashpw(pwd.encode('utf-8'), salt)
print(hashedPassword)
