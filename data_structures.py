import re
from collections import UserDict, defaultdict
from datetime import datetime


DATE_FORMAT = '%d.%m.%Y'


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(phone):
        return re.fullmatch(r'\d{10}', phone) is not None


class Birthday(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"Birthday must be in {DATE_FORMAT} format")
        super().__init__(value)

    @staticmethod
    def validate(birthday):
        try:
            datetime.strptime(birthday, DATE_FORMAT)
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {self.birthday.value if self.birthday else 'Not set'}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_birthdays_per_week(self):
        today = datetime.today()
        birthdays = defaultdict(list)

        for user in self.data.values():
            user_name = user.name.value
            if user.birthday:
                birthday_date = datetime.strptime(user.birthday.value, DATE_FORMAT)
                birthday_this_year = birthday_date.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days
                if delta_days <= 7:
                    day_of_week = birthday_this_year.weekday()
                    if day_of_week == 5 or day_of_week == 6:
                        day_of_week = 0
                    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][
                        day_of_week]
                    birthdays[day_name].append(user_name)

        return birthdays


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення кількох контактів
    contact_1 = Record("Анна")
    contact_2 = Record("Олексій")
    contact_3 = Record("Марія")

    # Додавання телефонів до контактів
    contact_1.add_phone("0987654321")
    contact_2.add_phone("1234567890")
    contact_3.add_phone("9876543210")

    # Додавання днів народження до контактів
    contact_1.add_birthday("11.03.1111")
    contact_2.add_birthday("15.03.1544")
    contact_3.add_birthday("20.03.2000")

    # Додавання контактів до адресної книги
    book.add_record(contact_1)
    book.add_record(contact_2)
    book.add_record(contact_3)

    # Використання функції get_birthdays_per_week для визначення, кого потрібно привітати на наступному тижні
    birthdays_next_week = book.get_birthdays_per_week()


