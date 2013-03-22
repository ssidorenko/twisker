import time


def get_interval_number(ts, duration):
    """Returns the number of the current interval.

    Args:
        ts: The timestamp to convert
        duration: The length of the interval
    Returns:
        int: interval number.
    """
    return int(time.mktime(ts.timetuple()) / duration)
