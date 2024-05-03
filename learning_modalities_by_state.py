import datetime as dt
import pandas

STATE_CODES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

DATE_FORMAT = "%m/%d/%Y"

MODALITIES = ["In Person", "Hybrid", "Remote"]


def is_valid_state_code(state_code: str) -> bool:
    """
    Check if a state code is valid
    :param state_code: str, state code
    :return: bool, True if the state code is valid, False otherwise
    """
    return state_code in STATE_CODES


def is_valid_date(date: str) -> bool:
    """
    Check if a date is valid
    :param date: str, date in the format "MM/DD/YYYY"
    :return: bool, True if the date is valid, False otherwise
    """
    try:
        dt.datetime.strptime(date, DATE_FORMAT)
        return True
    except ValueError:
        return False


def get_state_code_input(prompt="State (2 letter code or 'all'): ", error_message="Invalid state code.") -> str:
    """
    Get a valid state code from the user or "ALL" for all states
    :return: str, valid state code or "ALL"
    """
    state_code = input(prompt).upper()

    while not is_valid_state_code(state_code) and state_code != "ALL":
        print(error_message)
        state_code = input(prompt).upper()

    return state_code


def get_date_input(prompt="Enter a date (MM/DD/YYYY): ", error_message="Invalid date.") -> dt.datetime:
    """
    Get a valid date from the user
    :return: dt.datetime, valid date
    """
    date = input(prompt)

    while not is_valid_date(date):
        print(error_message)
        date = input(prompt)

    return dt.datetime.strptime(date, DATE_FORMAT)


def get_school_count(data: pandas.DataFrame, state_code: str, date: dt.datetime, modality=None):
    """
    Get the number of schools in a state on a given date
    :param data: pandas.DataFrame, data
    :param state_code: str, state code or "ALL"
    :param date: dt.datetime, date
    :param modality: str, learning modality or None
    :return: int, number of schools
    """
    filtered_data = data[data["week"] == date.strftime("%m/%d/%Y %I:%M:%S %p")]

    if state_code != "ALL":
        filtered_data = filtered_data[filtered_data["state"] == state_code]

    if modality:
        filtered_data = filtered_data[filtered_data["learning_modality"] == modality]

    return int(filtered_data["operational_schools"].sum())


def get_student_count(data, state_code, date, modality=None):
    """
    Get the number of students in a state on a given date
    :param data: pandas.DataFrame, data
    :param state_code: str, state code or "ALL"
    :param date: dt.datetime, date
    :param modality: str, learning modality or None
    :return: int, number of schools
    """
    filtered_data = data[data["week"] == date.strftime("%m/%d/%Y %I:%M:%S %p")]

    if state_code != "ALL":
        filtered_data = filtered_data[filtered_data["state"] == state_code]

    if modality:
        filtered_data = filtered_data[filtered_data["learning_modality"] == modality]

    return int(filtered_data["student_count"].sum())


def learning_modalities_by_state(data: pandas.DataFrame):
    """
    Print the number of schools and students in a state on a given date by learning modality
    :param data:  pandas.DataFrame, data
    """
    choice = 'y'
    while choice == 'y':
        print("Enter the two digit code (CA, MO, IL, TX, etc.) for a state or 'all' for all states.")

        state_code = get_state_code_input()
        date = get_date_input()

        overall_school_count = get_school_count(data, state_code, date)
        overall_student_count = get_student_count(data, state_code, date)

        modality_school_counts = {modality: get_school_count(data, state_code, date, modality) for modality in MODALITIES}
        modality_student_counts = {modality: get_student_count(data, state_code, date, modality) for modality in MODALITIES}

        print("-------------------------------")
        print(f"Date: {date.strftime(DATE_FORMAT)}")
        print(f"Description: {state_code}")

        print(f"{overall_school_count:,} schools")
        print(f"{overall_student_count:,} students")

        print("Schools per modality:")
        for modality, count in modality_school_counts.items():
            print(f" * {count:,} ({count / overall_school_count:.1%}) {modality}")

        print("Students per modality:")
        for modality, count in modality_student_counts.items():
            print(f" * {count:,} ({count / overall_student_count:.1%}) {modality}")

        print("-------------------------------")

        choice = input("Would you like to continue? (y/n): ")
        while choice.lower() not in ['y', 'n']:
            print("Invalid choice. Please enter 'y' or 'n'.")
            choice = input("Would you like to continue? (y/n): ")


if __name__ == '__main__':
    from load_data import load_data

    data = load_data("data.csv")
    learning_modalities_by_state(data)




