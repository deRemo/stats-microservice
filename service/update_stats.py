#from service.models import Stats
from json import loads, dumps
from collections import defaultdict


def init_stories_stats(stories):
    # Given a list of stories computes the stats

    # TODO: Before the update check presence of a new user
    
    count_stories = defaultdict(int)
    # Convert json to python
    list_stories = loads(stories)

    # Counting the number of stories for each user
    for story in list_stories:
        count_stories[story["author_id"]] += 1

    for k, v in count_stories.items():
        print(k)

    return count_stories

def update_reactions_stats():

    return
