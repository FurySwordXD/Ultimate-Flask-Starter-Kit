from datetime import datetime
from settings import app, db
from hashlib import sha256

def init_db(db):
    def save(model):
        db.session.add(model)
        db.session.commit()

    db.Model.save = save

init_db(db)

class User(db.Model):

    __tablename__ = "Users"

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    auth_token = db.Column(db.String)

    def __init__(self, username="", password=""):
        self.username = username
        self.update_password(password)
        self.auth_token = ""

    def __repr__(self):
        return '<User %r Pass %r>' % (self.username, self.password)

    def update_password(self, password: str):
        self.password = sha256(password.encode()).hexdigest()

    def obtain_auth_token(self):
        self.auth_token = sha256( (self.username + str(datetime.now().timestamp())).encode() ).hexdigest()
        self.save()
        return self.auth_token
    
    def clear_auth_token(self):
        self.auth_token = ""
        self.save()

    @staticmethod
    def create_fields():
        return {'username': 'text', 'password': 'password', 'confirm password': 'password'}

    @staticmethod
    def login_fields():
        return {'username': 'text', 'password': 'password'}

    def serialize(self):
        return {'username': self.username}



if __name__ == "__main__":
    db.create_all()
    #user = User.query.filter_by(username="admin").first()
    User(username="admin", password="admin").save()
    print(User.query.all())