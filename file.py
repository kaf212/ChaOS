from dataclasses import dataclass

from csv_handling import return_user_names
import os


@dataclass
class File:
    name: str
    type: str
    owner: str


def create_file(owner):
    file_object = create_file_object(owner)
    path = 'ChaOS_Users/' + file_object.owner + '/' + file_object.name + file_object.type
    f = open(path, 'w')
    f.close()
    # f.flush()
    # os.fsync(f.fileno())
    # f.close()
    #f.flush()
    #os.fsync(f.fileno())


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
        input_type = input('Filetype > ')
        if input_type not in ['.txt']:
                print('Invalid filetype, try again: ')
        else:
            type = input_type
            type_invalid = False

    owner = owner.name

    new_file = File(name, type, owner)

    return new_file





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





