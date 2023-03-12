import csv
import os
import time

import ChaOS_constants
from encryption import encrypt_str, decrypt_str
from file import create_dir
from system import syslog
from user import create_user_object, enter_username
from input import list_selection_options
from colors import print_warning, print_success


def login():
    """
    I know the code be mad ugly.
    :return User object:
    """
    username = None
    while username is None:
        input_username = input('Username (type /register to create new account) > ')
        dev_object = None

        if input_username.startswith('dev'):  # This is to me removed before release (You bet your ass I'll forget)
            if input_username.endswith('k'):
                dev_object = create_user_object('kaf221122', None, 'dev')
                print_success('Successfully logged in as developer kaf221122! ')
            elif input_username.endswith('n'):
                dev_object = create_user_object('NextToNothing', None, 'dev')
                print_success('Successfully logged in as developer NextToNothing! ')
            if dev_object:
                return dev_object

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
                print_warning('User not found, try again: ')

    print(f'\n-- {username} --')
    tries = 3
    while tries > 0:
        input_password = input('Password > ')
        if input_password != decrypt_str(password):
            tries -= 1
            print_warning('Wrong password, try again: ')
        else:
            break

    if tries <= 0:
        print('You haven entered too many wrong passwords. ')
        time.sleep(2)
        exit()

    user_object = create_user_object(username, password, account_type)

    return user_object


def create_user(username: str, password: str, account_type: str):
    if account_type not in ChaOS_constants.VALID_ACCOUNT_TYPES:
        raise ValueError('Invalid user account type given. ')

    if username in ['..', '...']:
        raise Exception('Invalid username, stop doing the "..." thing. ')
    if os.path.isdir(f'A/ChaOS_Users/{username}'):
        print_warning(f'Cannot create user, directory name already taken. ')
    else:
        os.mkdir(f'A/ChaOS_Users/{username}')
        temp_user_obj = create_user_object(username, password, account_type)
        for subdir in ChaOS_constants.STANDARD_USER_SUBDIRS:
            create_dir(user=temp_user_obj, name=subdir, dir=f'A/ChaOS_Users/{username}', dir_type='personal')
        with open('users.csv', 'a+', encoding="utf-8") as csv_file:
            attributes = ['username', 'password', 'account type']
            csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
            csv_writer.writerow({'username': username, 'password': encrypt_str(password), 'account type': account_type})
            csv_file.close()
        syslog('creation', f'created user "{username}"')


def create_user_ui(user=None, cmd_split=None):
    input_username = enter_username()

    password_invalid = True
    while password_invalid:
        input_password = input('Enter a password > ')
        pw_confirmation = input('Confirm your password > ')
        if input_password == pw_confirmation:
            password_invalid = False
        else:
            print_warning("Your passwords don't match, try again: ")

    if user is None:
        create_user(input_username, input_password, 'standard')
        print_success(f'User "{input_username}" was successfully created. ')
    else:
        while True:
            input_account_type = input('Enter an account type > ').lower()
            if input_account_type not in ChaOS_constants.VALID_ACCOUNT_TYPES:
                list_selection_options(input_account_type, ChaOS_constants.VALID_ACCOUNT_TYPES)
                continue
            if input_account_type == 'admin' and cmd_split[len(cmd_split) - 1] == 'sudo':
                create_user(input_username, input_password, input_account_type)
                print_success(f'User "{input_username}" was successfully created. ')
                break

            elif user.account_type not in ['admin', 'dev'] and input_account_type == 'admin':
                print_warning('You need administrator privileges to create a new admin. ')
                continue

            elif user.account_type != 'dev' and input_account_type == 'dev':
                print_warning('You need developer privileges to create a new dev. ')

            else:
                create_user(input_username, input_password, input_account_type)
                print_success(f'User "{input_username}" was successfully created. ')
                break
