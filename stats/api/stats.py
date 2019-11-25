from flask import Blueprint, jsonify
from stats.models import Stats
from stats.extensions import db
from stats.utility import errors

import flask_jwt_extended as jwt 

stats = Blueprint('stats', __name__)

BP_ID = 0

@stats.route('/stats', methods=['GET'])
@jwt.jwt_required
def get_statistics_by_id(func_id=0):
    '''
    Retrieves all the statistics from a given user
    Returns:
        200 -> User statistics retrieved successfully
        404 -> User not found
    '''
    stat = Stats.query.get(jwt.get_jwt_identity()['id'])
    
    if stats is None:
        return errors.response(f'{BP_ID}{func_id}1')

    return jsonify(stat)
