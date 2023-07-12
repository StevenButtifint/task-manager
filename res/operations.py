from datetime import datetime, timedelta
from res.constants import *


def get_today_date():
    return datetime.today().strftime('%Y/%m/%d')


def get_weekday_index():
    dt = datetime.now()
    return dt.weekday()


def get_day_difference(first_date, second_date):
    if first_date == DATE_BLANK:
        return 0
    else:
        d1 = datetime.strptime(first_date, "%Y/%m/%d")
        d2 = datetime.strptime(second_date, "%Y/%m/%d")
        delta = d2 - d1
        return delta.days


def get_last_week_dates():
    today = datetime.today()
    last_week = today - timedelta(days=1)
    weekday = last_week.weekday()

    last_week_dates = []
    for d in range(7, 0, -1):
        last_date = last_week - timedelta(days=(weekday + d) % 7)
        last_week_dates.append(last_date.strftime('%Y/%m/%d'))
    return last_week_dates
