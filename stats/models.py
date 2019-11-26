from flask_sqlalchemy import SQLAlchemy
from stats.extensions import db

class Stats(db.Model):
    '''
    Models the statistics retrieved from the whole infrastructure
    '''
    __tablename__ = 'stats'
    author_id = db.Column(db.Integer, primary_key=True)

    likes = db.Column(db.Integer, default=0, nullable=False)
    dislikes = db.Column(db.Integer, default=0, nullable=False)

    stories_written = db.Column(db.Integer, default=0, nullable=False)

    n_dice = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
    
    def get_stats(self):
        return {
            'likes': self.likes,
            'dislikes': self.dislikes,
            'n_stories': self.stories_written,
            'avg_dice': self.n_dice/self.stories_written
        }
