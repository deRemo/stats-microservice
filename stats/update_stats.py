from stats.models import Stats
from json import loads, dumps
from collections import defaultdict
from stats.extensions import db
import datetime as dt
from stats import errors


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

def update_stories_stats(stories):
    # It receives a list of the last stories
    list_stories = loads(stories)
    for story in list_stories:
        stat = Stats.query.filter_by(story["author_id"])
        if stat:
            # User has alredy statistics
            try:
                stat.stories_written += 1
                # Compute the average incrementally
                stat.avg_ndice += (len(story["dice_set"])-stat.avg_ndice)/(stat.stories_written)
                stat.stories_per_day = (1+stat.stories_per_day)/((stat.last_activity-stat.last_activity).days+1)
                stat.last_activity = dt.datetime.now()
                stat.is_active = True
                db.session.add(stat)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return errors.response('411')
    # TODO: When a user is registered the stats should be initialized
    return

def update_reactions_received_stats(reactions, author_id):
    # TODO: need the author of the story!
    # Given the list of reactions for a story
    list_reactions = loads(reactions)
    for reaction in list_reactions:
        stat = Stats.query.filter_by(author_id)
        if stat:
            try:
                stat.likes_received += reaction["likes"]
                stat.dislikes_received += reaction["dislikes"]
                db.session.add(stat)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return errors.response('411')
    return

def update_reactions_given_stats(reactions, user_id):
    # Given the list of reactions given by an author
    list_reactions = loads(reactions)
    for reaction in list_reactions:
        stat = Stats.query.filter_by(user_id)
        if stat:
            try:
                stat.likes_given += reaction["likes"]
                stat.dislikes_given += reaction["dislikes"]
            except Exception as e:
                print(e)
                db.session.rollback()
                return errors.response('411')
    return

