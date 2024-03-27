from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_date_range(day, month, year):

    if day == 0:
        date_to_get = datetime(year, month, 1)
        start_date = date_to_get - relativedelta(day=1)
        end_date = date_to_get - relativedelta(day=31)
    else:
        start_date = datetime(year, month, day)
        end_date = datetime(year, month, day)

    return start_date.date(), end_date.date()
