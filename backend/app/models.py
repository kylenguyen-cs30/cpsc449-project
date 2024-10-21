from app import db


from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    homeAddress = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)

    def __init__(self, email, firstName, lastName, password, homeAddress):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.homeAddress = homeAddress
        self.set_password(password)

    # Set password_hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.userName} created>"
