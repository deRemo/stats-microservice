from flask import jsonify

MOCK_STORY_1 = {
    "id": 0,
    "text": "Hello world",
    "date": "2019-11-20",
    "likes": 0,
    "dislikes": 0,
    "theme": "default",
    "dice_set": [
    "world"
    ],
    "deleted": False,
    "is_draft": False,
    "author_id": 1
}

MOCK_STORY_2 = {
    "id": 1,
    "text": "What a wonderful day",
    "date": "2019-11-20",
    "likes": 3,
    "dislikes": 0,
    "theme": "default",
    "dice_set": [
    "day", "wonderful"
    ],
    "deleted": False,
    "is_draft": False,
    "author_id": 1
}

MOCK_STORY_3 = {
    "id": 2,
    "text": "Writing a story",
    "date": "2019-11-20",
    "likes": 3,
    "dislikes": 0,
    "theme": "default",
    "dice_set": [
    "story"
    ],
    "deleted": False,
    "is_draft": False,
    "author_id": 2
}


def test_stories_stats(update_stats):
    stories = jsonify([MOCK_STORY_1, MOCK_STORY_2, MOCK_STORY_3])
    counter = update_stats.init_stories_stats(stories)

    assert counter[1] == 1
    
