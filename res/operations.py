from datetime import datetime


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')


def get_weekday_index():
    dt = datetime.now()
    return dt.weekday()
