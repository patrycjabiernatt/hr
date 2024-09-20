class Address:
    def __init__(self, country: str, city: str, street: str, postal_code: str):
        self.country = country
        self.city = city
        self.street = street
        self.postal_code = postal_code


class Employee:
    def __init__(self, first_name: str, last_name: str, birthday: str, pesel: str, address: Address):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.pesel = pesel
        self.address = address
