from flask import Blueprint

search = Blueprint('search', __name__)

@search.route('/stories', methods=['GET'])
def get_stories():
    pass


@search.route('/stories/<id>', methods=['GET'])
def get_story(id):
    pass


@search.route('/signup', methods=['POST'])
def signup():
    pass

@search.route('/stats/<id>', methods=['GET'])
def get_statistics_by_id(id):
    pass
