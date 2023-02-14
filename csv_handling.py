import csv


def return_user_names():
    with open('users.csv', 'r') as csv_file:
        attributes = ['name', 'password']
        next(csv_file)  # skip attribute header
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

        usernames = []
        for line in csv_reader:
            usernames.append(line['name'])

    return usernames
