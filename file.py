from dataclasses import dataclass

from csv_handling import return_user_names
import os


@dataclass
class File:
    name: str
    type: str
    owner: str


def create_file_object(owner):
    name = None
    name_invalid = True
    while name_invalid:
        input_name = input('Filename > ')
        if ' ' in input_name or "'" in input_name:
            print('Invalid filename, try again: ')
        else:
            name = input_name
            name_invalid = False

    type = None
    type_invalid = True
    while type_invalid:
        input_type = input('Filename > ')
        if input_type not in ['.txt']:
                print('Invalid filename, try again: ')
        else:
            type = input_type
            name_invalid = False

    owner = owner.name

    new_file = File(name, type, owner)

    return new_file


def create_file(file_object):
    pass


def initialize_user_directories():
    try:
        os.mkdir('ChaOS_Users')
    except FileExistsError:
        pass

    usernames = return_user_names()

    for username in usernames:
        path = 'ChaOS_Users/' + username
        try:
            os.mkdir(path)
        except FileExistsError:
            pass





