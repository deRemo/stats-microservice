from flask import Blueprint, jsonify
from stats.models import Stats
from stats.extensions import db

stats = Blueprint('stats', __name__)

@stats.route('/stats/<id>', methods=['GET'])
def get_statistics_by_id(id):
    '''
    Retrieves all the statistics from a given user
    Returns:
        200 -> User statistics retrieved successfully
        400 -> User not found
    '''
    stat = Stats.query.filter_by(author_id=id)
    print(stat)
    #stats = _retrieve_stats(stat)
    
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

