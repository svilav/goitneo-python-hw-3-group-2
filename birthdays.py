from datetime import datetime
from collections import defaultdict


def get_birthdays_per_week(users):
    """
    Given a list of users, print the names of the users whose birthday is in the next 7 days, grouped by day of the week.
    Args:
        users: list of dictionaries, each dictionary contains the name and birthday of a user.
    Returns:
        None
    """
    today = datetime.today().date()
    birthdays = defaultdict(list)

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days <= 7:
            day_of_week = birthday_this_year.weekday()

            if day_of_week == 5 or day_of_week == 6:
                day_of_week = 0

            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day_of_week]
            birthdays[day_name].append(name)

    for day, names in birthdays.items():
        print(f"{day}: {', '.join(names)}")


if __name__ == "__main__":
    users = [
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
        {"name": "Jan Koum", "birthday": datetime(1976, 2, 24)},
        {"name": "B B", "birthday": datetime(1997, 2, 26)},
        {"name": "A A", "birthday": datetime(1997, 2, 27)},
        {"name": "A C", "birthday": datetime(1997, 2, 25)},
    ]
    get_birthdays_per_week(users)
