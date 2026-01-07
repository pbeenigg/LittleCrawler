
from enum import Enum
from typing import NamedTuple

from src.utils import zhihu_const as zhihu_constant


class SearchTime(Enum):
    """
    Search time range
    """
    DEFAULT = ""  # No time limit
    ONE_DAY = "a_day"  # Within one day
    ONE_WEEK = "a_week"  # Within one week
    ONE_MONTH = "a_month"  # Within one month
    THREE_MONTH = "three_months"  # Within three months
    HALF_YEAR = "half_a_year"  # Within half a year
    ONE_YEAR = "a_year"  # Within one year


class SearchType(Enum):
    """
    Search result type
    """
    DEFAULT = ""  # No type limit
    ANSWER = zhihu_constant.ANSWER_NAME  # Answers only
    ARTICLE = zhihu_constant.ARTICLE_NAME  # Articles only
    VIDEO = zhihu_constant.VIDEO_NAME  # Videos only


class SearchSort(Enum):
    """
    Search result sorting
    """
    DEFAULT = ""  # Default sorting
    UPVOTED_COUNT = "upvoted_count"  # Most upvoted
    CREATE_TIME = "created_time"  # Latest published
