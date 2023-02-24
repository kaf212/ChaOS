import shutil
from dataclasses import dataclass

from csv_handling import return_user_names
import os
from datetime import datetime
import ChaOS_constants


def find_file(user):
    while True:
        input_filename = input('Filename + type > ')
        directory = os.fsencode(f'A/ChaOS_Users/{user.name}')
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


def create_file(dir, name, user):
    name_valid = True
    for char in [' ', '..', '...', '/', "'", '"']:
        if char in name:
            name_valid = False

    if name_valid:
        path = dir + '/' + name
        now = datetime.now()
        now = datetime.strftime(now, '%d.%m.%Y %H:%M')
        if not check_file_existence(path):
            header_line = None
            header = None
            if path.endswith('.txt'):
                header = f'{name} created on the {now} by {user.name} with ChaOS {ChaOS_constants.CHAOS_VERSION}'
                header_line = ''
                for i in range(len(list(header))):
                    header_line += '-'
                with open(path, 'w', 1) as f:
                    f.write(header_line + '\n')
                    f.write(header + '\n')
                    f.write(header_line + '\n')
                    f.write('\n')
                    f.close()
        else:
            print(f'{name} already exists in {dir}. ')
    else:
        print(f'{name} contains illegal characters. ')


def read_txt(dir, name):
    path = dir + '/' + name
    with open(path, 'r') as f:
        print(f'-- {name} --\n')
        print(f.read())
        print(f'\n-- {name} --\n')
        f.close()


def initialize_user_directories():
    try:
        os.makedirs('A/ChaOS_Users', 0o777)
    except FileExistsError:
        pass

    usernames = return_user_names()

    for username in usernames:
        path = 'A/ChaOS_Users/' + username
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

    for user_dir in os.listdir('A/ChaOS_Users'):  # delete directories of non existent users
        if user_dir not in return_user_names():
            shutil.rmtree(f'A/ChaOS_Users/{user_dir}')


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


def delete_file(path):
    if check_file_existence(path):
        os.remove(path)
    else:
        print("File not found. ")


def edit_txt(path):
    user_text = input('Write > ')
    with open(path, 'a+') as f:
        f.write('\n')
        f.write(user_text)
        f.close()


def create_dir(dir, name):
    name_valid = True
    for char in [' ', '..', '.', '...', '/', "'", '"']:
        if char in name:
            name_valid = False

    if name_valid:
        if not dir.endswith('/'):
            path = dir + '/' + name
        else:
            path = dir + name
        try:
            os.mkdir(path, 0o777)
        except FileExistsError:
            print(f'The directory "{name}" already exists. ')
        else:
            print(f'Directory "{name}" has been created in {dir}. ')
    else:
        print(f'"{name}" contains illegal characters. ')


def validate_dir_access(path, dir_owners, user, cmd_split):
    path_split = split_path(path)
    parent_dir = ''
    i = 0
    for item in path_split:  # this ugly snippet takes the full path and reduces it to the user's personal dir
        if i < 5:  # in order to validate it in dir_owners,
            parent_dir += item  # for example: A/ChaOS_Users/kaf221122/subdir1/subdir2 ==> A/ChaOS_Users/kaf221122
            i += 1

    try:
        if dir_owners[parent_dir] == user.name:
            return True
        elif dir_owners[parent_dir] == 'all users':
            return True
    except KeyError:
        if user.account_type in ['admin', 'dev']:
            return True
        if cmd_split[len(cmd_split) - 1] == 'sudo':
            return True
        else:
            return False
    else:
        return True


def split_path(path):
    path_split_total = []
    while True:
        path_split = path.partition('/')
        path_split_total.append(path_split[0])
        path_split_total.append(path_split[1])
        path = path_split[2]
        if '/' not in path_split[2]:
            path_split_total.append(path_split[2])
            break

    return path_split_total
