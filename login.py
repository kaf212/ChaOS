import csv

from user import create_user_object


def login():
    """
    I know the code be mad ugly.
    :return User object:
    """
    username = None
    while username is None:
        input_username = input('Username (type /register to create new account) > ')
        if input_username == '/register':
            name_taken = True
            while name_taken:
                input_username = input('Enter a username > ')

                with open('users.csv', 'r') as csv_file:
                    attributes = ['name', 'password']
                    next(csv_file)  # skip attribute header
                    csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

                    name_taken = False
                    for line in csv_reader:
                        if line['name'] == input_username:
                            name_taken = True

                    if name_taken:
                        input('This Username is already taken. ')

            password = None
            password_invalid = True
            while password_invalid:
                input_password = input('Enter a password > ')
                pw_connfirmation = input('Confirm your password > ')
                if input_password == pw_connfirmation:
                    password_invalid = False
                    password = input_password
                else:
                    input("Your passwords don't match, try again: ")

            input(f'User {input_username} was successfully created. ')
            create_user(input_username, password)

        with open('users.csv', 'r') as csv_file:
            attributes = ['name', 'password']
            next(csv_file)  # skip attribute header
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

            for line in csv_reader:
                if line['name'] == input_username:
                    username = line['name']
                    password = line['password']

            if username is None:
                print('User not found, try again: ')

    print(f'\n-- {username} --')
    tries = 3
    while tries > 0:
        input_password = input('Password > ')
        if input_password != password:
            tries -= 1
            print('Wrong password, try again: ')
        else:
            break

    if tries <= 0:
        input('You haven entered too many wrong passwords. ')
        exit()

    user_object = create_user_object(username, password)

    return user_object


def create_user(username, password):
    with open('users.csv', 'a+') as csv_file:
        attributes = ['username', 'password']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writerow({'username': username, 'password': password})
        csv_file.close()


def clean_user_csv():
    """
    Genocide tool for test users.
    :return:
    """
    with open('users.csv', 'w') as csv_file:
        attributes = ['username', 'password']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        csv_writer.writerow({'username': 'kaf212', 'password': '1234'})
        csv_writer.writerow({'username': 'NextToNothing', 'password': 'asdf'})
        csv_writer.writerow({'username': 'Custoomer31', 'password': 'svp'})
        csv_writer.writerow({'username': 'Seve', 'password': 'minecraft'})
        csv_file.close()
