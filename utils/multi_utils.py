import datetime


def calender_years():
    now = datetime.datetime.now()
    year = now.year
    year_list_range = []
    for item in range(year -  1, year + 1):
        year_list_range.append(str(item))
    return tuple(year_list_range)