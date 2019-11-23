from flask import Blueprint, jsonify
from stats.models import Stats
from stats.extensions import db

search = Blueprint('search', __name__)

@search.route('/stats/<id>', methods=['GET'])
def get_statistics_by_id(id):
    '''
    Retrieves all the statistics from a given user
    Returns:
        200 -> User statistics retrieved successfully
        400 -> User not found
    '''

    try:
        example = Stats()
        example.author_id = 1
        example.likes_given = 2
        example.dislikes_given = 0
        example.likes_received = 5
        example.dislikes_received = 3
        example.stories_written = 15
        example.avg_ndice = 4.50
        example.stories_per_day = 2
        #example.date_of_entry = str(dt.datetime.now())
        #example.last_activity = str(dt.datetime.now())
        example.is_active = True
        db.session.add(example)
        db.session.commit()
    except:
        db.session.rollback()

    stat = Stats.query.filter_by(author_id=id)
    print(stat)
    stats = _retrieve_stats(stat)

    
    return jsonify(stat)

'''
def _retrieve_stats(stat):
    stats = {}
    stats['likes_given'] = stat.likes_given
    stats['dislikes_given'] = 
    stats['likes_received'] = 
    stats['dislikes_received']
    stats['stories_written']
    stats['avg_ndice']
    stats['stories_per_day']
    stats['date_of_entry']
    stats['last_activity']
    stats['is_active']'''

