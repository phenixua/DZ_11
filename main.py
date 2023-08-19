from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return value.isdigit() and len(value) == 10

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_phone(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid phone number")


class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday")
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        return isinstance(value, datetime) and value <= datetime.now()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_birthday(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid birthday")


class Record:
    def __init__(self, name: Name, phones: list, emails: list=None, birthday: Birthday=None):
        self.name = name
        self.phones = phones if phones else []
        self.emails = emails if emails else []
        self.birthday = birthday

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def delete_phone(self, phone):
        new_phones = [p for p in self.phones if p.value != phone]
        self.phones = new_phones

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.now().date()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()

        days_left = (next_birthday - today).days
        return days_left

class AddressBook(UserDict):
    def __init__(self, per_page=10):
        super().__init__()
        self.per_page = per_page

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self):
        keys = list(self.keys())
        current_page = 0

        while current_page * self.per_page < len(keys):
            start_index = current_page * self.per_page
            end_index = (current_page + 1) * self.per_page
            page_records = [self[key] for key in keys[start_index:end_index]]
            yield page_records
            current_page += 1

# Тестування класів
if __name__ == "__main__":
    name = Name('Bill')
    phone = Phone('1234567890')
    birthday = Birthday(datetime(2000, 5, 10))  # Приклад дня народження
    rec = Record(name, [phone], birthday=birthday)  
    ab = AddressBook()
    ab.add_record(rec)  

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    print('All Ok')
