from dataclasses import dataclass
from input import input_selection
from encryption import encrypt_str, decrypt_str
import csv


@dataclass
class User:
    name: str
    password: str
    account_type: str
    # more coming soon


def create_user_object(username, password, account_type):
    user = User(username, password, account_type)
    return user


def edit_user(cmd_split):
    if not check_user_existence(cmd_split[2]):
        print(f'The user "{cmd_split[2]}" does not exist. ')
    else:
        while True:
            edit_selection = input_selection(['n', 'p', 'a'], ['name', 'password', 'account type'],
                                             'What do you want to edit? ')
            if edit_selection == 'n':
                input_username = enter_username()
                write_user_csv('name', cmd_split[2], input_username)
            else:
                print("You can't edit passwords or account types yet, the function does not differentiate "
                      "between users!!!")
                break
            # TODO: make edit_user() work for passwords and account types without always changing it for every user.


def write_user_csv(attribute, old_value, new_value):
    if attribute in ['password', 'account type']:
        raise Exception('WRITE USER_CSV IS NOT READY FOR PW OR ACCOUNT TYPE CHANGES!!! ')

    if old_value in ['name', 'password', 'account type'] or new_value in ['name', 'password', 'account type']:
        raise Exception('Tried overwriting attribute header in users.csv. ')

    if attribute not in ['name', 'password', 'account type']:
        raise ValueError(f'Invalid attribute "{attribute}" given. ')
    if attribute == 'account type' and (
            old_value not in ['standard', 'admin', 'dev'] or new_value not in ['standard', 'admin', 'dev']):
        raise ValueError('Invalid account type given. ')

    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        csv_iter = ''.join([i for i in csv_file])

        if attribute == 'password':
            csv_iter = csv_iter.replace(encrypt_str(old_value), encrypt_str(new_value))
        csv_iter = csv_iter.replace(old_value, new_value)

        f = open('users.csv', 'w', encoding='utf-8')
        f.writelines(csv_iter)
        f.close()


def check_user_existence(username: str):
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ['name']
        next(csv_file)  # skip attribute header
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

        name_taken = False
        for line in csv_reader:
            if line['name'] == username:
                name_taken = True

        if name_taken:
            return True
        else:
            return False


def enter_username():
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

        name_taken = check_user_existence(input_username)
        if name_taken:
            print(f'The username "{input_username}" is already taken. ')
        else:
            return input_username
