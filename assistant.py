from data_structures import Record, Phone, AddressBook


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input. Please provide the correct number of arguments."

    return inner


@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Please provide both name and phone number.")
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book):
    if len(args) != 2:
        raise ValueError("Please provide both name and new phone number.")
    name, new_phone = args
    record = book.find(name)
    if record:
        record.phones = [Phone(new_phone)]
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    else:
        raise KeyError


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args, book):
    print(args)
    if len(args) != 2:
        raise ValueError("Please provide both name and birthday.")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value
    else:
        return "Birthday not set."


def show_all(book):
    if not book.data:
        return "No contacts stored."
    return '\n'.join(str(record) for record in book.data.values())


def show_birthdays_next_week(book):
    birthdays = book.get_birthdays_per_week()
    for day, names in birthdays.items():
        print(f"{day}: {', '.join(names)}")


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            show_birthdays_next_week(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()


# hello
# add John 1234567890
# add Jane 0987654321
# change John 1112223333
# phone John
# add-birthday John 01.01.1990
# add-birthday Jane 13.03.1998
# show-birthday John
# all
# birthdays
# close
