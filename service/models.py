from flask_sqlalchemy import SQLAlchemy
from service.extensions import db

class Stats(db.Model):
    '''
    Models the statistics retrieved from the whole infrastructure
    '''
    __tablename__ = 'stats'
    autor_id = db.Column(db.Integer, primary_key=True)
    
    like_given = db.Column(db.Integer)
    dislike_given = db.Column(db.Integer)

    like_received = db.Column(db.Integer)
    dislike_received = db.Column(db.Integer)

    stories_written = db.Column(db.Integer)