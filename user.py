from dataclasses import dataclass
from input import input_selection, list_selection_options
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
            new_value = None
            old_value = None
            if edit_selection == 'n':
                new_value = enter_username()
                old_value = cmd_split[2]
                edit_selection = 'name'
            elif edit_selection == 'p':
                while True:
                    pw = input('Enter the new password > ')
                    pw_confirmation = input('Confirm the new password > ')
                    if pw == pw_confirmation:
                        break
                    else:
                        print("Your passwords don't match, try again: ")
                new_value = pw
                edit_selection = 'password'
            elif edit_selection == 'a':
                while True:
                    input_acc_type = input('Enter the new account type: ')
                    if input_acc_type not in ['standard', 'admin', 'dev']:
                        list_selection_options(input_acc_type, ['standard', 'admin', 'dev'])
                    else:
                        break
                new_value = input_acc_type
                edit_selection = 'account type'

            alter_user_csv(username=cmd_split[2], attribute=edit_selection, old_value=old_value, new_value=new_value)


def alter_user_csv(username, attribute, old_value, new_value):
    if old_value in ['name', 'password', 'account type'] or new_value in ['name', 'password', 'account type']:
        raise Exception('Tried overwriting attribute header in users.csv. ')
    if attribute not in ['name', 'password', 'account type']:
        raise ValueError(f'Invalid attribute "{attribute}" given. ')
    old_value_invalid = False
    new_value_invalid = False
    if attribute == 'account type' and (old_value not in ['standard', 'admin', 'dev']):
        old_value_invalid = True
    if attribute == 'account type' and (new_value not in ['standard', 'admin', 'dev']):
        new_value_invalid = True

    if old_value_invalid and new_value_invalid:
        raise ValueError('Invalid account type given. ')

    if attribute == 'name':
        with open('users.csv', 'r', encoding='utf-8') as csv_file:
            attributes = ['name', 'password', 'account type']
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
            csv_iter = ''.join([i for i in csv_file])

            csv_iter = csv_iter.replace(old_value, new_value)

            with open('users.csv', 'w', encoding='utf-8') as f:
                f.writelines(csv_iter)
                f.close()

    if attribute == 'password':
        alter_user_password(username, new_value)
    if attribute == 'account type':
        alter_user_account_type(username, new_value)


def alter_user_account_type(username: str, new_account_type: str):
    if new_account_type not in ['standard', 'admin', 'dev']:
        raise ValueError(f'Invalid account type "{new_account_type}" given.')

    temp_dict_list = []
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        next(csv_reader)
        for line in csv_reader:
            if line['name'] == username:
                line['account type'] = new_account_type
            temp_dict_list.append(line)

    with open('users.csv', 'w', encoding='utf-8') as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        for line in temp_dict_list:
            csv_writer.writerow(line)
        csv_file.close()


def alter_user_password(username: str, new_password: str):
    """
    ALRIGHT MF, SECOND TRY.
    :return:
    """
    temp_dict_list = []
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        next(csv_reader)
        for line in csv_reader:
            if line['name'] == username:
                line['password'] = encrypt_str(new_password)
            temp_dict_list.append(line)

    with open('users.csv', 'w', encoding='utf-8') as csv_file:
        attributes = ['name', 'password', 'account type']
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        for line in temp_dict_list:
            csv_writer.writerow(line)
        csv_file.close()


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
