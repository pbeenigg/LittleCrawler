

import time
from datetime import datetime, timedelta, timezone


def get_current_timestamp() -> int:
    """
    Get current timestamp (13 digits): 1701493264496
    :return:
    """
    return int(time.time() * 1000)


def get_current_time() -> str:
    """
    Get current time: '2023-12-02 13:01:23'
    :return:
    """
    return time.strftime('%Y-%m-%d %X', time.localtime())

def get_current_time_hour() -> str:
    """
    Get current time with hour: '2023-12-02-13'
    :return:
    """
    return time.strftime('%Y-%m-%d-%H', time.localtime())

def get_current_date() -> str:
    """
    Get current date: '2023-12-02'
    :return:
    """
    return time.strftime('%Y-%m-%d', time.localtime())


def get_time_str_from_unix_time(unixtime):
    """
    Unix integer timestamp ==> datetime string
    :param unixtime:
    :return:
    """
    if int(unixtime) > 1000000000000:
        unixtime = int(unixtime) / 1000
    return time.strftime('%Y-%m-%d %X', time.localtime(unixtime))


def get_date_str_from_unix_time(unixtime):
    """
    Unix integer timestamp ==> date string
    :param unixtime:
    :return:
    """
    if int(unixtime) > 1000000000000:
        unixtime = int(unixtime) / 1000
    return time.strftime('%Y-%m-%d', time.localtime(unixtime))


def get_unix_time_from_time_str(time_str):
    """
    Time string ==> Unix integer timestamp, precise to seconds
    :param time_str:
    :return:
    """
    try:
        format_str = "%Y-%m-%d %H:%M:%S"
        tm_object = time.strptime(str(time_str), format_str)
        return int(time.mktime(tm_object))
    except Exception as e:
        return 0
    pass


def get_unix_timestamp():
    return int(time.time())


def rfc2822_to_china_datetime(rfc2822_time):
    # Define RFC 2822 format
    rfc2822_format = "%a %b %d %H:%M:%S %z %Y"

    # Convert RFC 2822 time string to datetime object
    dt_object = datetime.strptime(rfc2822_time, rfc2822_format)

    # Convert datetime object timezone to China timezone
    dt_object_china = dt_object.astimezone(timezone(timedelta(hours=8)))
    return dt_object_china


def rfc2822_to_timestamp(rfc2822_time):
    # Define RFC 2822 format
    rfc2822_format = "%a %b %d %H:%M:%S %z %Y"

    # Convert RFC 2822 time string to datetime object
    dt_object = datetime.strptime(rfc2822_time, rfc2822_format)

    # Convert datetime object to UTC time
    dt_utc = dt_object.replace(tzinfo=timezone.utc)

    # Calculate Unix timestamp from UTC time
    timestamp = int(dt_utc.timestamp())

    return timestamp


if __name__ == '__main__':
    # Example usage
    _rfc2822_time = "Sat Dec 23 17:12:54 +0800 2023"
    print(rfc2822_to_china_datetime(_rfc2822_time))
