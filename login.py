import csv
import os

from encryption import encrypt_str, decrypt_str
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
                invalid_chars = [' ', '/', '.', '(', ')', '|', '"', "'"]
                input_username = input('Enter a username > ')
                name_valid = True
                for char in invalid_chars:
                    if char in input_username:
                        name_valid = False
                if not name_valid or input_username == '':
                    print('This username contains illegal characters. ')
                    continue

                with open('users.csv', 'r', encoding='utf-8') as csv_file:
                    attributes = ['name']
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
            create_user(input_username, password, 'standard')

        with open('users.csv', 'r', encoding='utf-8') as csv_file:
            attributes = ['name', 'password', 'account type']
            next(csv_file)  # skip attribute header
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

            for line in csv_reader:
                if line['name'] == input_username:
                    username = line['name']
                    password = line['password']
                    account_type = line['account type']

            if username is None:
                print('User not found, try again: ')

    print(f'\n-- {username} --')
    tries = 3
    input_password = None
    while tries > 0:
        input_password = input('Password > ')
        if input_password != decrypt_str(password):
            tries -= 1
            print('Wrong password, try again: ')
        else:
            break

    if tries <= 0:
        input('You haven entered too many wrong passwords. ')
        exit()

    user_object = create_user_object(username, password, account_type)

    return user_object


def create_user(username, password, account_type):

    if account_type not in ['admin', 'standard']:
        raise ValueError('Invalid user account type given. ')

    if username in ['..', '...']:
        raise Exception('Invalid username, stop doing the ... thing. ')

    os.mkdir(f'A/ChaOS_Users/{username}')

    with open('users.csv', 'a+', encoding="utf-8") as csv_file:
        attributes = ['username', 'password', 'account type']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writerow({'username': username, 'password': encrypt_str(password), 'account type': account_type})
        csv_file.close()


def reset_user_csv():
    """
    Genocide tool for test users.
    :return:
    """
    with open('users.csv', 'w', encoding="utf-8") as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        csv_writer.writerow({'name': 'kaf221122', 'password': encrypt_str('1234'), 'account type': 'admin'})
        csv_writer.writerow({'name': 'NextToNothing', 'password': encrypt_str('asdf'), 'account type': 'standard'})
        csv_writer.writerow({'name': 'Custoomer31', 'password': encrypt_str('svp'), 'account type': 'standard'})
        csv_writer.writerow({'name': 'Seve', 'password': encrypt_str('minecraft'), 'account type': 'standard'})
        csv_writer.writerow({'name': 'Manu', 'password': encrypt_str('st.lutzi'), 'account type': 'standard'})
        csv_file.close()
