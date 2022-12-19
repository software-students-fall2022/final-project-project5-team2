import pytest
from app import get_random_prompt
from app import sort_posts
from app import get_time_from

from datetime import datetime, date

class Tests:

    def test_sanity_check(self):
        """
        Test debugging... making sure that we can run a simple test that always passes.
        """
        expected = True # the value we expect to be present
        actual = True # the value we see in reality
        assert actual == expected, "Expected True to be equal to True!"

    def test_sort_by_likes(self):
        """
        Test if sort_posts by likes sorts by likes
        """
        post1 = {
                '_id': 1,
                'votes': 10,
                'time_created': date.fromisoformat('2020-01-01')
            }
        post2 = {
                '_id': 2,
                'votes': 8,
                'time_created': date.fromisoformat('2021-01-01')
            }
        post3 = {
                '_id': 3,
                'votes': 40,
                'time_created': date.fromisoformat('2022-01-01')
            }
        posts = [post1, post2, post3]
        expected = [post3, post1, post2]
        sorted_posts = sort_posts(posts, 'likes')
        assert sorted_posts == expected, f'Expected sorted posts to be {expected}, instead it was {sort_posts}'

    def test_sort_by_dates(self):
        """
        Test if sort_posts by most recent sorts by likes
        """
        post1 = {
                '_id': 1,
                'votes': 10,
                'time_created': date.fromisoformat('2020-01-01')
            }
        post2 = {
                '_id': 2,
                'votes': 8,
                'time_created': date.fromisoformat('2021-01-01')
            }
        post3 = {
                '_id': 3,
                'votes': 40,
                'time_created': date.fromisoformat('2022-01-01')
            }
        posts = [post1, post2, post3]
        expected = [post3, post2, post1]
        sorted_posts = sort_posts(posts, 'recent')
        assert sorted_posts == expected, f'Expected sorted posts to be {expected}, instead it was {sort_posts}'

    def test_get_time_days(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "3 days ago"
        time_str = get_time_from(date.fromisoformat('2022-01-01'), date.fromisoformat('2022-01-04'))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'
    
    def test_get_time_week(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "1 week ago"
        time_str = get_time_from(date.fromisoformat('2022-01-01'), date.fromisoformat('2022-01-08'))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'
    
    def test_get_time_months(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "3 months ago"
        time_str = get_time_from(date.fromisoformat('2022-01-01'), date.fromisoformat('2022-04-06'))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'
    
    def test_get_time_years(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "5 years ago"
        time_str = get_time_from(date.fromisoformat('2017-01-01'), date.fromisoformat('2022-04-06'))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'
    
    def test_get_time_seconds(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "20 seconds ago"
        time_str = get_time_from(datetime(2022, 1, 1, 0, 0, 10), datetime(2022, 1, 1, 0, 0, 30))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'

    def test_get_time_hour(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "1 hour ago"
        time_str = get_time_from(datetime(2022, 1, 1, 0, 0, 10), datetime(2022, 1, 1, 1, 0, 10))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'

    def test_get_time_minutes(self):
        """
        Test if get_time_from returns correct value
        """
        expected = "10 minutes ago"
        time_str = get_time_from(datetime(2022, 1, 1, 0, 0, 10), datetime(2022, 1, 1, 0, 10, 10))
        assert time_str == expected, f'Expected {expected}, instead was {time_str}'
