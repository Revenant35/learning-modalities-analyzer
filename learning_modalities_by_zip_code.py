import pandas
import datetime as dt

DATE_FORMAT = "%m/%d/%Y"

MODALITIES = ["In Person", "Hybrid", "Remote"]


def is_valid_zip_code(zip_code: int) -> bool:
    """
    Check if a zip code is valid
    :param zip_code: int, zip code
    :return: bool, True if the zip code is valid, False otherwise
    """
    return 10000 <= zip_code <= 99999


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


def get_zip_code_input(prompt="Enter a zip code: ", error_message="Invalid zip code.") -> int:
    """
    Get a valid zip code from the user
    :return: int, valid zip code
    """
    zip_code = int(input(prompt))

    while not is_valid_zip_code(zip_code):
        print(error_message)
        zip_code = int(input(prompt))

    return zip_code


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


def learning_modalities_by_zip_code(data: pandas.DataFrame):
    choice = 'y'
    while choice == 'y':
        print("Enter the zip code and date to get information about a school district.")
        zip_code = get_zip_code_input()
        date = get_date_input()

        district_data = data[(data["zip_code"] == zip_code) & (data["week"] == date.strftime("%m/%d/%Y %I:%M:%S %p"))]

        if district_data.empty:
            print("No data found for the given zip code and date.")
        else:
            district_nces_id = district_data["district_nces_id"].iloc[0]
            district_name = district_data["district_name"].iloc[0]
            learning_mode = district_data["learning_modality"].iloc[0]
            num_schools = int(district_data["operational_schools"].iloc[0])
            num_students = int(district_data["student_count"].iloc[0])
            city = district_data["city"].iloc[0]
            state = district_data["state"].iloc[0]

            print(f"District NCES ID: {district_nces_id:07d}")
            print(f"School name: {district_name}")
            print(f"Date: {date.strftime(DATE_FORMAT)}")
            print(f"Learning Mode: {learning_mode}")
            print(f"Number of schools: {num_schools}")
            print(f"Number of students: {num_students}")
            print(f"City: {city}")
            print(f"State: {state}")
            print(f"Zip Code: {zip_code}")

        choice = input("Would you like to get information for another school district (y/n)? ").lower()
        while choice not in ["y", "n"]:
            print("Invalid choice. Please try again.")
            choice = input("Would you like to get information for another school district (y/n)? ").lower()


if __name__ == '__main__':
    from load_data import load_data

    data = load_data("data.csv")
    learning_modalities_by_zip_code(data)
