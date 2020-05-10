from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, user_dict):
        self.name = user_dict['name']
        self.email = user_dict['email']
        self.bio = user_dict['bio']
        self.keywords = user_dict['keywords']
        self.image = user_dict['image']
        self.authenticated = False

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False






