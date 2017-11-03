from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime())
    email = db.Column(db.String(), nullable=True, unique=True)
    phone = db.Column(db.String(), nullable=True)
    twId = db.Column(db.String(), nullable=True)
    fbId = db.Column(db.String(), nullable=True)
    fbToken = db.Column(db.String(), nullable=True)
    twToken = db.Column(db.String(), nullable=True)
    positiveMessage = db.Column(db.String(), nullable=True)
    negativeMessage = db.Column(db.String(), nullable=True)
    triggerDate = db.Column(db.DateTime(), nullable=True)
    distFromPoll = db.Column(db.String(), nullable=True)

    def __init__(self, name, date, email, phone, twId, fbId, fbToken, twToken, positiveMessage, negativeMessage, triggerDate, distFromPoll):
        self.name = name
        self.date = date
        self.email = email
        self.phone = phone
        self.twId = twId
        self.fbId = fbId
        self.fbToken = fbToken
        self.twToken = twToken
        self.positiveMessage = positiveMessage
        self.negativeMessage = negativeMessage
        self.triggerDate = triggerDate
        self.distFromPoll = distFromPoll

    def __repr__(self):
        return '<id {}>'.format(self.id)
