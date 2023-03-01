import csv
import os

import ChaOS_constants
from encryption import encrypt_str, decrypt_str
from user import create_user_object, enter_username
from input import list_selection_options


def login():
    """
    I know the code be mad ugly.
    :return User object:
    """
    username = None
    while username is None:
        input_username = input('Username (type /register to create new account) > ')
        if input_username == '/register':
            create_user_ui()

        with open('users.csv', 'r', encoding='utf-8') as csv_file:
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
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


def create_user(username: str, password: str, account_type: str):
    if account_type not in ChaOS_constants.VALID_ACCOUNT_TYPES:
        raise ValueError('Invalid user account type given. ')

    if username in ['..', '...']:
        raise Exception('Invalid username, stop doing the "..." thing. ')

    os.mkdir(f'A/ChaOS_Users/{username}')

    with open('users.csv', 'a+', encoding="utf-8") as csv_file:
        attributes = ['username', 'password', 'account type']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writerow({'username': username, 'password': encrypt_str(password), 'account type': account_type})
        csv_file.close()


def create_user_ui(user=None, cmd_split=None):

    input_username = enter_username()

    input_password = None
    password_invalid = True
    while password_invalid:
        input_password = input('Enter a password > ')
        pw_confirmation = input('Confirm your password > ')
        if input_password == pw_confirmation:
            password_invalid = False
        else:
            input("Your passwords don't match, try again: ")

    if user is None:
        create_user(input_username, input_password, 'standard')
        input(f'User {input_username} was successfully created. ')
    else:
        while True:
            input_account_type = input('Enter an account type > ').lower()
            if input_account_type not in ChaOS_constants.VALID_ACCOUNT_TYPES:
                list_selection_options(input_account_type, ChaOS_constants.VALID_ACCOUNT_TYPES)
                continue
            if input_account_type == 'admin' and cmd_split[len(cmd_split) - 1] == 'sudo':
                create_user(input_username, input_password, input_account_type)
                input(f'User {input_username} was successfully created. ')
                break

            elif user.account_type not in ['admin', 'dev'] and input_account_type == 'admin':
                print('You need administrator privileges to create a new admin. ')
                continue

            elif user.account_type != 'dev' and input_account_type == 'dev':
                print('You need developer privileges to create a new dev. ')

            else:
                create_user(input_username, input_password, input_account_type)
                input(f'User {input_username} was successfully created. ')
                break
