import bcrypt
pwd = '1'
salt = bcrypt.gensalt()
hashedPassword = bcrypt.hashpw(pwd.encode('utf-8'), salt)
print(hashedPassword)
