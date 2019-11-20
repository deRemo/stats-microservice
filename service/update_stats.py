#from service.models import Stats
from json import loads, dumps
from collections import defaultdict
import datetime as dt


def init_stories_stats(stories):
    # Given a list of stories computes the stats

    stats = {}

    count_stories = defaultdict(int)
    count_likes = defaultdict(int)
    count_dislikes = defaultdict(int)

    count_dice = defaultdict(int)
    avg_ndice = defaultdict(int)
    story_frequency = defaultdict(int)
    is_active = defaultdict(int)

    user_stories = defaultdict(list)
    # Convert json to python
    list_stories = loads(stories)

    # Computing statistics for each user
    for story in list_stories:
        author = story["author_id"]
        user_stories[author].append(story)
        count_stories[author] += 1
        count_likes[author] += story["likes"]
        count_dislikes[author] += story["dislikes"]
        count_dice[author] += len(story["dice_set"])

    stats['number_stories'] = count_stories
    stats['total_likes'] = count_likes
    stats['total_dislikes'] = count_dislikes
    
    # Stories contains the list of stories for an author
    for author, stories in user_stories.items():
        avg_ndice[author] = count_dice[author]/count_stories[author]
        first_story = dt.datetime.strptime(stories[-1]["date"], '%Y-%m-%d')
        n_days = (dt.datetime.now()-first_story).days+1
        story_frequency[author] = len(stories)/n_days

        delta = dt.datetime.now()-dt.timedelta(days=7)
        last_story = dt.datetime.strptime(stories[0]["date"], '%Y-%m-%d')
        is_active[author] = True if delta < last_story else False

    stats['avg_ndice'] = avg_ndice
    stats['story_frequency'] = story_frequency
    stats['is_active'] = is_active

    return stats

def update_reactions_stats():
    # TODO: Before the update, check presence of a new user

    return

