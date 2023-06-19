from datetime import datetime


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')


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
