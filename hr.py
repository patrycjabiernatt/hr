from tabulate import tabulate
import sys
import csv
import os.path
import os
import numpy as np
from models import Address, Employee


def print_menu(options) -> None:
    print("Menu:")
    print(tabulate(options, headers=['Akcja', 'Opis'], tablefmt='rounded_grid'))


def find_all_employees() -> list[Employee]:
    if not os.path.exists('employees.csv'):
        return []

    employee_list: list[Employee] = []
    with open('employees.csv', 'r', encoding='UTF-8', newline='') as file:
        reader = csv.DictReader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        for row in reader:
            address = Address(row['country'], row['city'], row['street'], row['postal_code'])
            employee = Employee(row['first_name'], row['last_name'], row['birthday'], row['pesel'], address)
            # Dodanie jako obiektu do listy
            employee_list.append(employee)

    return employee_list


def append_employee_to_file(e: Employee):
    # import os
    file_empty = os.stat('employees.csv').st_size == 0
    with open('employees.csv', 'a', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        if file_empty:
            writer.writerow(
                ["country", "city", "street", "postal_code", "first_name", "last_name", "birthday", "pesel"])
        writer.writerow(
            [e.address.country, e.address.city, e.address.street, e.address.postal_code, e.first_name, e.last_name,
             e.birthday, e.pesel]
        )


def create_address() -> Address:
    country = input("Kraj: ")
    city = input("Miasto: ")
    street = input("Ulica: ")
    postal_code = input("Kod pocztowy: ")
    return Address(country, city, street, postal_code)


def add_employee():
    first_name = input("Podaj imię pracownika: ")
    last_name = input("Podaj nazwisko pracownika: ")
    pesel = input("Podaj PESEL: ")
    birthday = input("Podaj datę urodzenia [YYYY-MM-dd]: ")

    print(10 * '-', 'Tworzenie Adresu', 10 * '-')

    address = create_address()
    employee = Employee(first_name, last_name, birthday, pesel, address)

    employee_list = find_all_employees()

    if [e for e in employee_list if e.pesel == pesel]:
        print("Nie można dodać 2 pracowników z takim samym nr. PESEL!")
        return

    append_employee_to_file(employee)


def save_all_file(employees: list[Employee]):
    headers = ["country", "city", "street", "postal_code", "first_name", "last_name", "birthday", "pesel"]
    with open('employees.csv', 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        for e in employees:
            writer.writerow(
                [e.address.country, e.address.city, e.address.street, e.address.postal_code, e.first_name, e.last_name,
                 e.birthday, e.pesel]
            )
        file.flush()


def delete_employee(employee: Employee, all_employees: list[Employee]):
    after_remove_employee = [e for e in all_employees if e.pesel != employee.pesel]
    save_all_file(after_remove_employee)
    print(f"Pracownik {employee.first_name} {employee.last_name} został usunięty poprawnie")


def edit_employee(employee: Employee, all_employees: list[Employee]):
    for e in all_employees:
        if e.pesel == employee.pesel:
            print("Jeżeli nie ma zmiany danych ENTER")
            first_name = input("Podaj imię pracownika: ") or e.first_name
            last_name = input("Podaj nazwisko pracownika: ") or e.last_name
            birthday = input("Podaj datę urodzenia [YYYY-MM-dd]: ") or e.birthday
            country = input("Kraj: ") or e.address.country
            city = input("Miasto: ") or e.address.city
            street = input("Ulica: ") or e.address.street
            postal_code = input("Kod pocztowy: ") or e.address.postal_code

            e.first_name = first_name
            e.last_name = last_name
            e.birthday = birthday
            e.address.country = country
            e.address.city = city
            e.address.street = street
            e.address.postal_code = postal_code

    save_all_file(all_employees)

def search_employee():
    search_pesel = input("Proszę podać PESEL do wyszukiwania: ")
    all_employees = find_all_employees()
    found = [e for e in all_employees if e.pesel == search_pesel]

    if not found:
        print(f"Pracownik o numerze PESEL {search_pesel} nie został znaleziony!")
        return

    print_employee_table(found)
    found = found[0]

    choice_map = {
        "1": delete_employee,
        "2": edit_employee
    }
    menu_options = [
        ["1", "Usuń Pracownika"],
        ["2", "Edytuj Pracownika"],
        ["0", "Powrót"]
    ]

    while True:
        print_menu(menu_options)
        decision = input('>\t')

        if decision == '0':
            break
        elif decision not in choice_map:
            print("Proszę wybrać poprawną akcję")
        else:
            choice_map[decision](found, all_employees)
            break


def print_employee_table(employee_list: list[Employee]) -> None:
    table_data = [
        (emp.first_name, emp.last_name, emp.pesel, emp.birthday,
         f"{emp.address.country} {emp.address.city}, {emp.address.street} {emp.address.postal_code}") for emp in
        employee_list
    ]
    print(
        tabulate(table_data, headers=['Imię', 'Nazwisko', 'PESEl', 'Data urodzenia', 'Adres'], tablefmt='rounded_grid'))


def list_all_employees():
    all_employees = find_all_employees()
    all_employees.sort(key=lambda emp: emp.last_name)
    print_employee_table(all_employees)


def filter_employees():
    last_name_filter = input("Proszę podać część nazwiska: ")
    all_employees = find_all_employees()
    filtered_list = [e for e in all_employees if last_name_filter.lower() in e.last_name.lower()]
    print_employee_table(filtered_list)


def exit():
    sys.exit()


if __name__ == '__main__':
    menu_options = [
        ["1", "Dodaj Pracownika"],
        ["2", "Wyszukaj Pracownika"],
        ["3", "Wyświetl Wszystkich Pracowników"],
        ["4", "Filtruj Pracowników"],
        ["0", "Exit"]
    ]
    choice_map = {
        "1": add_employee,
        "2": search_employee,
        "3": list_all_employees,
        "4": filter_employees,
        "0": exit
    }

    while True:
        print_menu(menu_options)
        decision = input(">\t")

        if decision not in choice_map:
            print("Proszę wybrać poprawną akcję!")
        else:
            choice_map[decision]()
