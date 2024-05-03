import pandas

CSV_HEADERS = [
    "district_nces_id",
    "district_name",
    "week",
    "learning_modality",
    "operational_schools",
    "student_count",
    "city",
    "state",
    "zip_code"
]


def load_data(filename):
    """
    Load data from a CSV file
    :param filename: str, path to the CSV file
    :return: pandas.DataFrame containing the data
    """
    return pandas.read_csv(filename)


def is_valid_column_headers(filename):
    """
    Check if the file is a valid CSV file
    :param filename: str, path to the file
    :return: bool, True if the file is a valid CSV file, False otherwise
    """
    try:
        with open(filename) as file:
            header = file.readline().strip().split(",")
            return header == CSV_HEADERS
    except FileNotFoundError:
        return False
