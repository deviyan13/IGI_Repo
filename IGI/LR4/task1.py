"""
Task 1: Phone Book Serialization Application
Program Name: PhoneBook Manager
Version: 1.0
Developer: Anufryieu Dzianis
Date: 2025-04-27

Description:
This program implements a phone book application that stores data using a dictionary and 
serializes it into CSV and Pickle formats. It supports searching for abonents (contacts) whose 
phone numbers begin with digits entered by the user.
"""

import csv
import pickle
from inputs_check import input_int, input_int_with_condition

class PhoneBook:
    """
    PhoneBook class implements a phone book.

    Features:
    - Uses an internal dictionary (_phone_book) to store phone-number: name pairs.
    - Demonstrates dynamic attributes (instance attribute _phone_book) and static attributes (version).
    - Implements property getters/setters, special methods (e.g. __str__), and uses inheritance.
    """
    # Static attribute (class attribute)
    version = "1.0"

    def __init__(self):
        """
        Initializes the phone book with default entries.
        """
        self._phone_book = {
            "3996280": "Denis",
            "8739453": "Eugene",
            "8374630": "Daria",
            "6125394": "Maria"
        }

    @property
    def phone_book(self) -> dict:
        """
        Property getter for the phone book.

        Returns:
            dict: The current dictionary representing the phone book.
        """
        return self._phone_book

    @phone_book.setter
    def phone_book(self, value: dict) -> None:
        """
        Property setter to update the phone book.

        Args:
            value (dict): New dictionary to update the phone book with.
        """
        self._phone_book = value.copy()

    def write_by_csv(self, filename: str) -> None:
        """
        Writes phone book entries to a CSV file.

        Args:
            filename (str): Path to the CSV file.
        """
        with open(filename, 'w', newline='', encoding="utf-8") as pf:
            writer = csv.writer(pf)
            for phone, name in self.phone_book.items():
                writer.writerow([phone, name])

    def read_from_csv(self, filename: str) -> None:
        """
        Reads phone book entries from a CSV file and updates the phone book.

        Args:
            filename (str): Path to the CSV file.
        """
        try:
            with open(filename, 'r', newline='', encoding="utf-8") as pf:
                reader = csv.reader(pf)
                self.phone_book = {row[0]: row[1] for row in reader}
        except:
            print('Ошибка загрузки данных в телефонную книгу')

    def dump_by_pickle(self, filename: str) -> None:
        """
        Serializes the phone book using pickle and writes it to a file.

        Args:
            filename (str): Path to the pickle file.
        """
        with open(filename, 'wb') as pf:
            pickle.dump(self._phone_book, pf)

    def get_dict_by_pickle(self, filename: str) -> None:
        """
        Reads the phone book from a pickle file and updates the phone book.

        Args:
            filename (str): Path to the pickle file.
        """
        try:
            with open(filename, 'rb') as pf:
                self.phone_book = dict(pickle.load(pf))
        except:
            print('Ошибка загрузки данных в телефонную книгу')

    def get_abonents_start_with(self, prefix: str) -> list:
        """
        Returns a list of abonents whose phone numbers start with a given prefix.

        Args:
            prefix (str): The starting digits to search for.

        Returns:
            list: List of names matching the criteria.
        """
        return [name for phone, name in self.phone_book.items() if phone.startswith(prefix)]

    def __str__(self) -> str:
        """
        Overrides the string representation to display phone book contents in a friendly format.

        Returns:
            str: A formatted string of phone book entries.
        """
        entries = [f"{phone}: {name}" for phone, name in sorted(self.phone_book.items())]
        return "\n".join(entries)


def task1() -> None:
    """
    Runs the phone book application. This function handles:
      - Serialization (CSV & Pickle) and reading from files.
      - User prompt for searching abonents by phone number prefix.
      - Repeated execution and exception handling.
    """

    print(
        "Task 1 menu:\n"
           "1. Записать книгу в файл .csv\n"
           "2. Записать книгу в файл с помощью pickle\n"
           "3. Загрузить книгу из файла .csv\n"
           "4. Загрузить книгу из файла с помошью pickle\n"
           "5. Найти абонентов по первым цифрам\n"
           "6. Выход в главное меню)\n")

    phone_book = PhoneBook()
    csv_filename = 'files/task1.csv'
    pkl_filename = 'files/task1.pkl'

    while True:
        item = input_int_with_condition('Введите пункт меню: ', lambda x: 0 < x < 7)
        match item:
            case 1:
                phone_book.write_by_csv(csv_filename)
                print(f'Телефонная книга загружена в {csv_filename}')
            case 2:
                phone_book.dump_by_pickle(pkl_filename)
                print(f'Телефонная книга загружена в {pkl_filename}')
            case 3:
                phone_book.read_from_csv(csv_filename)
                print(f'Телефонная книга прочитана из {csv_filename}')
            case 4:
                phone_book.get_dict_by_pickle(pkl_filename)
                print(f'Телефонная книга прочитана из {pkl_filename}')
            case 5:
                first_numbers = str(input_int('Введите первые цифры номера для поиска: '))
                abonents = phone_book.get_abonents_start_with(first_numbers)
                if len(abonents) > 0:
                    print(f'Абонеты с номером на {first_numbers}:')
                    for ab in abonents:
                        print(ab, end=' ')
                else:
                    print('Нет таких абонентов.')
                print()
            case 6:
                break