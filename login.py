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
            create_user_ui()

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


def create_user(username: str, password: str, account_type: str):
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


def create_user_ui(user=None):
    name_taken = True
    input_username = None
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
        input_account_type = input('Enter an account type (admin or standard) > ').lower()
        if input_account_type not in ['admin', 'standard']:
            print(f'"{input_account_type}" is not a valid account type, try "admin" or "standard". ')
        elif user.account_type != 'admin' and input_account_type == 'admin':
            print('You need administrator privileges to create a new admin. ')
        else:
            create_user(input_username, input_password, input_account_type)
            input(f'User {input_username} was successfully created. ')

def reset_user_csv():
    """
    Genocide tool for test users.
    :return:
    """
    with open('users.csv', 'w', encoding="utf-8") as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        csv_writer.writerow(
            {'name': 'kaf221122', 'password': encrypt_str(decrypt_str('')), 'account type': 'admin'})
        csv_writer.writerow(
            {'name': 'NextToNothing', 'password': encrypt_str(decrypt_str('ËÙÎÌ')), 'account type': 'standard'})
        csv_writer.writerow(
            {'name': 'Custoomer31', 'password': encrypt_str(decrypt_str('ÙÜÚ')), 'account type': 'standard'})
        csv_writer.writerow(
            {'name': 'Seve', 'password': encrypt_str(decrypt_str('ÇÃÄÏÉØËÌÞ')), 'account type': 'standard'})
        csv_writer.writerow(
            {'name': 'Manu', 'password': encrypt_str(decrypt_str('ÙÞÆßÞÐÃ')), 'account type': 'standard'})
        csv_file.close()
