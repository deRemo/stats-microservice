from flask_sqlalchemy import SQLAlchemy
from service.extensions import db

class Stats(db.Model):
    '''
    Models the statistics retrieved from the whole infrastructure
    '''
    __tablename__ = 'stats'
    author_id = db.Column(db.Integer, primary_key=True)
    
    likes_given = db.Column(db.Integer)
    dislikes_given = db.Column(db.Integer)

    likes_received = db.Column(db.Integer)
    dislikes_received = db.Column(db.Integer)

    stories_written = db.Column(db.Integer)
