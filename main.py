from pathlib import Path

import pandas
import datetime as dt

from download_modalities import download_modalities
from learning_modalities_by_state import learning_modalities_by_state
from learning_modalities_by_zip_code import learning_modalities_by_zip_code
from list_dates import list_dates
from load_data import load_data, is_valid_column_headers

def get_yes_no(prompt):
    """
    Get a yes or no answer from the user
    :param prompt: str, prompt
    :return: str, "y" or "n"
    """
    choice = input(prompt)

    while choice not in ["y", "n"]:
        print("Invalid choice. Please try again.")
        choice = input(prompt)

    return choice

def is_valid_file(filename):
    return Path(filename).is_file() and is_valid_column_headers(filename)

def get_data_filename(prompt="Data file path: "):
    """
    Get the name of the data file from the user
    :return: str, name of the data file
    """
    filename = input(prompt)

    while not is_valid_file(filename):
        if not Path(filename).is_file():
            should_download_file = get_yes_no("File not found. Would you like to download it to this location (y/n)? ")
            if should_download_file == "y":
                download_modalities(filename)
                break
            else:
                print("File will not be downloaded. Please enter a valid file path.")
        elif not is_valid_column_headers(filename):
            print("Invalid file. Please try again.")
        else:
            print("Unexpected error. Please try again.")

        filename = input(prompt)

    return filename

def get_analysis_choice(prompt="Enter the number of the option (1, 2, 3, or 4): "):
    """
    Get the analysis choice from the user
    :return: int, analysis choice
    """
    choice = input(prompt)

    while choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please try again.")
        choice = input(prompt)

    return int(choice)


# Learning Modalities Analyzer
#
# Data file path: School_Learning_Modalities__2020-2021.csv
#
# Data analysis options:

if __name__ == '__main__':
    print("Learning Modalities Analyzer")

    filename = get_data_filename()
    data = load_data(filename)

    choice = 0
    while choice != 4:
        print("Data analysis options:\n")
        print("1. List dates")
        print("2. Learning modality by state on date")
        print("3. Learning modality by zip code on date")
        print("4. Exit\n")

        choice = get_analysis_choice()
        if choice == 1:
            list_dates(data)
        elif choice == 2:
            learning_modalities_by_state(data)
        elif choice == 3:
            learning_modalities_by_zip_code(data)
        elif choice == 4:
            print("Goodbye")
