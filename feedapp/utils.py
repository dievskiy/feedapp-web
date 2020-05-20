import calendar


def get_name_for_month(month):
    """
    get month name from number
    :param month: month in 1-based format
    :return: String name for month ex. January
    """
    return str(calendar.month_name[int(month)])
