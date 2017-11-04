from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime())
    email = db.Column(db.String(), nullable=True, unique=True)
    phone = db.Column(db.String(), nullable=True)
    twId = db.Column(db.String(), nullable=True, unique=True)
    fbId = db.Column(db.String(), nullable=True, unique=True)
    fbToken = db.Column(db.String(), nullable=True, unique=True)
    twToken = db.Column(db.String(), nullable=True, unique=True)
    positiveMessage = db.Column(db.String(), nullable=True)
    negativeMessage = db.Column(db.String(), nullable=True)
    triggerDate = db.Column(db.DateTime(), nullable=True)
    distFromPoll = db.Column(db.String(), nullable=True)
    referringUser = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
