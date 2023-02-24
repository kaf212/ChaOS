import csv
import ChaOS_constants


def return_user_names():
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
        next(csv_file)  # skip attribute header
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

        usernames = []
        for line in csv_reader:
            usernames.append(line['name'])

    return usernames


def return_users():
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
        next(csv_file)  # skip attribute header
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

        usernames = []
        for line in csv_reader:
            usernames.append(line)

    return usernames
