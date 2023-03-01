import os
from dataclasses import dataclass
import ChaOS_constants
from input import input_selection, list_selection_options
from encryption import encrypt_str
import csv
import time
from system import syslog

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
            edit_selection = input_selection(['n', 'p', 'a', 'x'], ['name', 'password', 'account type', 'done editing'],
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
                    if input_acc_type not in ChaOS_constants.VALID_ACCOUNT_TYPES:
                        list_selection_options(input_acc_type, ChaOS_constants.VALID_ACCOUNT_TYPES)
                    else:
                        break
                new_value = input_acc_type
                edit_selection = 'account type'

            elif edit_selection == 'x':
                break

            if edit_selection != 'x':
                alter_user_csv(username=cmd_split[2], attribute=edit_selection, old_value=old_value, new_value=new_value)
                syslog('alteration', f'Edited user "{cmd_split[2]}"')

            if edit_selection == 'name':
                print(f'Successfully renamed "{old_value}" to "{new_value}". ')
                time.sleep(1.5)
            if edit_selection == 'password':
                print(f'Successfully changed password of "{cmd_split[2]}". ')
                time.sleep(1.5)
            if edit_selection == 'account type':
                print(f'Succcessfully chnanged account type of "{cmd_split[2]}". ')
                time.sleep(1.5)


def alter_user_csv(username, attribute, old_value, new_value):
    if old_value in ChaOS_constants.USER_CSV_ATTRIBUTES or new_value in ChaOS_constants.USER_CSV_ATTRIBUTES:
        raise Exception('Tried overwriting attribute header in users.csv. ')
    if attribute not in ChaOS_constants.USER_CSV_ATTRIBUTES:
        raise ValueError(f'Invalid attribute "{attribute}" given. ')
    old_value_invalid = False
    new_value_invalid = False
    if attribute == 'account type' and (old_value not in ChaOS_constants.VALID_ACCOUNT_TYPES):
        old_value_invalid = True
    if attribute == 'account type' and (new_value not in ChaOS_constants.VALID_ACCOUNT_TYPES):
        new_value_invalid = True

    if old_value_invalid and new_value_invalid:
        raise ValueError('Invalid account type given. ')

    if attribute == 'name':
        os.rename(f'A/ChaOS_Users/{old_value}', f'A/ChaOS_Users/{new_value}')
        with open('users.csv', 'r', encoding='utf-8') as csv_file:
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            next(csv_file)
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
            csv_iter = ''.join([i for i in csv_file])

            csv_iter = csv_iter.replace(old_value, new_value)

            with open('users.csv', 'w', encoding='utf-8') as f:
                csv_writer = csv.DictWriter(f, fieldnames=attributes)
                csv_writer.writeheader()
                f.writelines(csv_iter)
                f.close()

    if attribute == 'password':
        alter_user_password(username, new_value)
    if attribute == 'account type':
        alter_user_account_type(username, new_value)


def alter_user_account_type(username: str, new_account_type: str):
    if new_account_type not in ChaOS_constants.VALID_ACCOUNT_TYPES:
        raise ValueError(f'Invalid account type "{new_account_type}" given.')

    temp_dict_list = []
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        next(csv_reader)
        for line in csv_reader:
            if line['name'] == username:
                line['account type'] = new_account_type
            temp_dict_list.append(line)

    with open('users.csv', 'w', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
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
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        next(csv_reader)
        for line in csv_reader:
            if line['name'] == username:
                line['password'] = encrypt_str(new_password)
            temp_dict_list.append(line)

    with open('users.csv', 'w', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
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
