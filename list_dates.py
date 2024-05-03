import datetime as dt
import pandas


def get_dates(data: pandas.DataFrame) -> pandas.Series:
    """
    Get the unique dates from the data
    :param data: pandas.DataFrame
    :return: pandas.Series containing the dates
    """
    return data["week"].unique()


def extract_date(date_string: str) -> dt.datetime:
    """
    Extract the date from a string
    :param date_string: str, date in the format "MM/DD/YYYY HH:MM:SS AM/PM"
    :return: datetime.datetime object
    """
    return dt.datetime.strptime(date_string, "%m/%d/%Y %I:%M:%S %p")


def format_date(date: pandas.DataFrame) -> str:
    """
    Format a date as a string
    :param date: datetime.datetime object
    :return: str, date in the format "MM/DD/YYYY HH:MM:SS AM/PM"
    """
    return date.strftime("%m/%d/%Y")


def list_dates(data: pandas.DataFrame) -> None:
    """
    List the unique dates in the data
    :param data: pandas.DataFrame
    """
    dates = get_dates(data)
    dates = [extract_date(date) for date in dates]
    dates = sorted(dates, reverse=True)
    dates = [format_date(date) for date in dates]

    for date in dates:
        print(date)


if __name__ == '__main__':
    from main import load_data

    data = load_data("data.csv")
    list_dates(data)
