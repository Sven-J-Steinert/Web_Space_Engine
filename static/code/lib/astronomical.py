import math
from datetime import timedelta


def calculate_sideral_degree(time):
    # Ref: Astronomical Algorithms, pg. 88
    jd = calculate_julian_date(time)
    T = (jd - 2451545) / 36525
    degrees = 280.46061837 + 360.98564736629 * (jd - 2451545)\
        + 0.000387933 * T**2 - T**3 / 38710000
    return degrees % 360


def calculate_julian_date(datetime):
    dt = timedelta(
        days=datetime.day, hours=datetime.hour,
        minutes=datetime.minute, seconds=datetime.second)
    days = dt.total_seconds() / timedelta(days=1).total_seconds()
    return date_to_jd(datetime.year, datetime.month, days)


def date_to_jd(year, month, day):
    """
    Convert a date to Julian Day.

    Examples
    --------
    Convert 6 a.m., February 17, 1985 to Julian Day

    >>> date_to_jd(1985,2,17.25)
    2446113.75

    """
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month

    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
            (year == 1582 and month < 10) or
            (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)

    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)

    D = math.trunc(30.6001 * (monthp + 1))
    jd = B + C + D + day + 1720994.5
    return jd
