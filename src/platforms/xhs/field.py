
from enum import Enum
from typing import NamedTuple


class FeedType(Enum):
    # Recommend
    RECOMMEND = "homefeed_recommend"
    # Fashion
    FASION = "homefeed.fashion_v3"
    # Food
    FOOD = "homefeed.food_v3"
    # Cosmetics
    COSMETICS = "homefeed.cosmetics_v3"
    # Movie and TV
    MOVIE = "homefeed.movie_and_tv_v3"
    # Career
    CAREER = "homefeed.career_v3"
    # Emotion
    EMOTION = "homefeed.love_v3"
    # Home
    HOURSE = "homefeed.household_product_v3"
    # Gaming
    GAME = "homefeed.gaming_v3"
    # Travel
    TRAVEL = "homefeed.travel_v3"
    # Fitness
    FITNESS = "homefeed.fitness_v3"


class NoteType(Enum):
    NORMAL = "normal"
    VIDEO = "video"


class SearchSortType(Enum):
    """Search sort type"""
    # Default
    GENERAL = "general"
    # Most popular
    MOST_POPULAR = "popularity_descending"
    # Latest
    LATEST = "time_descending"


class SearchNoteType(Enum):
    """Search note type"""
    # Default
    ALL = 0
    # Only video
    VIDEO = 1
    # Only image
    IMAGE = 2


class Note(NamedTuple):
    """Note tuple"""
    note_id: str
    title: str
    desc: str
    type: str
    user: dict
    img_urls: list
    video_url: str
    tag_list: list
    at_user_list: list
    collected_count: str
    comment_count: str
    liked_count: str
    share_count: str
    time: int
    last_update_time: int
