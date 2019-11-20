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

    avg_dice = db.Column(db.Float)
    stories_per_day = db.Column(db.Float)
    active_user = db.Column(db.Boolean)