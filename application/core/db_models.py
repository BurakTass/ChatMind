from application import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(), index=True)
    surname = db.Column(db.String(), index=True)
    email = db.Column(db.String(), index=True)
    password = db.Column(db.String(), index=True)


