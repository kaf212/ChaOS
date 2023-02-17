from dataclasses import dataclass

from csv_handling import return_user_names
import os
from datetime import datetime


@dataclass
class File:
    name: str
    type: str
    owner: str


def find_file(user):
    while True:
        input_filename = input('Filename + type > ')
        directory = os.fsencode(f'ChaOS_Users/{user.name}')
        found_file_name = None
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename == input_filename:
                found_file_name = os.fsdecode(file)
            else:
                continue
        if found_file_name:
            return found_file_name
        else:
            input('File not found. ')


def read_txt_old(filename, owner):
    path = 'ChaOS_Users/' + owner.name + '/' + filename
    with open(path, 'r') as f:
        print(f'-- {filename} --\n')
        print(f.read())
    # exit(read_txt(filename, owner))  #TODO: try implementing that when calling stuff in main


def create_file_old(owner):
    file_object = create_file_object(owner)
    path = 'ChaOS_Users/' + file_object.owner + '/' + file_object.name + file_object.type
    f = open(path, 'a+', 1)
    f.write(f'{file_object.name}{file_object.type} created on the {datetime.now()}')
    # f.flush()
    # os.fsync(f.fileno())
    f.close()


def create_file(dir, name):
    path = dir + '/' + name
    with open(path, 'w') as f:
        f.write(f'{name} created on the {datetime.now()}')
        # f.flush()
        # os.fsync(f.fileno())
        f.close()


def read_txt(dir, name):
    path = dir + '/' + name
    with open(path, 'r') as f:
        print(f'-- {name} --\n')
        print(f.read())
        f.close()


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


def validate_filetype(filename, valid_filetypes):
    ft_valid = False
    for filetype in valid_filetypes:
        if filename.endswith(filetype):
            ft_valid = True

    if not ft_valid:
        print(f'"{"." + filename.partition(".")[2]}" is not a valid filetype\n')

    return ft_valid


def check_file_existence(path):
    f_exists = os.path.isfile(path)
    return f_exists
