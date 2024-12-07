from app.mysql_connection import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(101), unique=True, nullable=False)
    homeAddress = db.Column(db.String(101), nullable=False)
    password_hash = db.Column(db.String(129), nullable=False)
    firstName = db.Column(db.String(101), nullable=False)
    lastName = db.Column(db.String(101), nullable=False)

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
        return f"<User {self.email} created>"


# public crum
class PublicCrum(db.Model):
    __tablename__ = "public_crums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(101), nullable=False)
    description = db.Column(db.String(101), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)

    def __init__(self, name, description, quantity, price) -> None:
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"<Public Crum {self.name} - Qty: {self.quantity}>"
