import logging
import shutil
import csv
from csv_handling import return_user_names, return_users
import os
from datetime import datetime
import ChaOS_constants
from user import create_user_object, User
import logging


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


def log_dir_metadata(user, dirname, access_permission, parent_dir):
    logging_format = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)
    """
    Path for metadata always is: parent_dir/metadata.csv, for example the metadata for A/ChaOS_Users/kaf221122 is in A/ChaOS_Users/metadata.csv
    """
    if access_permission not in [user.name, 'all_users', 'admins', 'devs']:
        raise ValueError(f'Invalid access permission "{access_permission}" given. ')

    if not os.path.isdir(parent_dir):
        raise NotADirectoryError(f'{parent_dir} is not a directory. ')

    md_path = f'{parent_dir}/metadata.csv'
    if not os.path.exists(md_path):
        with open(md_path, 'w') as md_csv:
            attributes = ['dirname', 'owner', 'owner account type', 'access permission']
            csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
            csv_writer.writeheader()
            md_csv.close()

    if not check_metadata_existence(user, dirname, access_permission, parent_dir):
        with open(md_path, 'a+') as md_csv:
            attributes = ['dirname', 'owner', 'owner_account_type', 'access_permission']
            csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
            csv_writer.writerow({'dirname': dirname, 'owner': user.name, 'owner_account_type': user.account_type,
                                 'access_permission': access_permission})
            md_csv.close()


def read_dir_metadata(dirname: str, parent_dir: str) -> tuple:
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
    if not os.path.isdir(parent_dir):
        raise NotADirectoryError(f'{parent_dir} is not a directory. ')

    md_path = f'{parent_dir}/metadata.csv'
    if os.path.exists(md_path):
        with open(md_path, 'r') as md_csv:
            attributes = ['dirname', 'owner', 'owner_account_type', 'access_permission']
            csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
            dir_metadata = None
            for line in csv_reader:
                if line['dirname'] == dirname:
                    dir_metadata = line
            if not dir_metadata:
                raise Exception(f'No metadata found for ')

            md_csv.close()

            return dir_metadata['owner'], dir_metadata['owner_account_type'], dir_metadata['access_permission']
    else:
        raise FileNotFoundError(f'metadata.csv not found in {md_path}. ')


def check_metadata_existence(user, dirname: str, access_permission: str, path: str) -> bool:
    md_path = f'{path}/metadata.csv'
    with open(md_path, 'r') as md_csv:
        attributes = ['dirname', 'owner', 'owner_account_type', 'access_permission']
        next(md_csv)
        csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
        for line in csv_reader:
            if line == {'dirname': dirname, 'owner': user.name, 'owner_account_type': user.account_type,
                        'access_permission': access_permission}:
                md_csv.close()
                return True
        return False


def read_txt(dir, name):
    path = dir + '/' + name
    with open(path, 'r') as f:
        print(f'-- {name} --\n')
        print(f.read())
        print(f'\n-- {name} --\n')
        f.close()


def initialize_user_directories():
    logging_format = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)
    try:
        os.makedirs('A/ChaOS_Users', 0o777)
    except FileExistsError:
        pass

    usernames = return_user_names()

    for username in usernames:
        path = 'A/ChaOS_Users/' + username
        if not os.path.exists(path):
            os.mkdir(path)

    # for user_dir in os.listdir('A/ChaOS_Users'):  # delete directories of non existent users
    #     if user_dir not in return_user_names():
    #         try:
    #             shutil.rmtree(f'A/ChaOS_Users/{user_dir}')  #TODO: make the programm delete deleted user's dirs, but not active user's non-personal dirs
    #         except NotADirectoryError:
    #             os.remove(f'A/ChaOS_Users/{user_dir}')

    for username in usernames:
        initialize_user_dir_metadata(username)


def initialize_user_dir_metadata(username):
    logging_format = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    all_users = return_users()

    for line in all_users:
        if line['name'] == username:
            temp_user_obj = create_user_object(username=line['name'], password='None', account_type=line['account type'])
            log_dir_metadata(user=temp_user_obj, dirname=temp_user_obj.name, parent_dir='A/ChaOS_Users',
                             access_permission=temp_user_obj.name)


def delete_metadata(dirname, parent_dir):
    md_path = f'{parent_dir}/metadata.csv'
    with open(md_path, 'r') as md_csv:
        attributes = ['dirname', 'owner', 'owner_account_type', 'access_permission']
        next(md_csv)
        csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
        temp_dict_list = []
        for line in csv_reader:
            if not line['dirname'] == dirname:
                temp_dict_list.append(line)
        md_csv.close()

    with open(md_path, 'w') as md_csv:
        attributes = ['dirname', 'owner', 'owner_account_type', 'access_permission']
        csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
        csv_writer.writeheader()
        for line in temp_dict_list:
            csv_writer.writerow(line)
        md_csv.close()


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


# delete dir kaf221122 "" "" "" sudo

def delete_dir(directory, dir_name, dir_owners):
    path = directory + '/' + dir_name
    try:
        shutil.rmtree(path)
        delete_metadata(dir_name, directory)
    except FileNotFoundError:
        print(f'The directory "{path}" does not exist')
    else:
        print(f'"{path}" was deleted successfully. ')


def edit_txt(path):
    user_text = input('Write > ')
    with open(path, 'a+') as f:
        f.write('\n')
        f.write(user_text)
        f.close()


def create_dir(user, dir, name, cmd_split=None):
    name_valid = True
    for char in [' ', '..', '.', '...', '/', "'", '"']:
        if char in name:
            name_valid = False

    if name_valid:
        access_permission = user.name # the default access permission is creator only
        if cmd_split:
            try:
                access_permission = cmd_split[3]
            except IndexError:
                pass

        if not dir.endswith('/'):
            path = dir + '/' + name
        else:
            path = dir + name
        try:
            os.mkdir(path, 0o777)
            log_dir_metadata(user, name, access_permission, dir)
        except FileExistsError:
            print(f'The directory "{name}" already exists. ')
        else:
            print(f'Directory "{name}" has been created in {dir}. ')
    else:
        print(f'"{name}" contains illegal characters. ')


def validate_dir_access(parent_dir: str, dirname: str, user, cmd_split: list) -> bool:
    fmt = ChaOS_constants.LOGGING_FORMAT
    logging.basicConfig(level=logging.DEBUG, format=fmt)

    if f'{parent_dir}/{dirname}' in ['A/','A', 'A/ChaOS_Users']:  # TODO: this looks dumb, check if it's not
        return True

    owner, owner_account_type, access_permission = read_dir_metadata(dirname, parent_dir)
    if access_permission == 'all_users':
        return True
    if access_permission == user.account_type:
        return True

    if user.account_type == 'dev':
        return True

    if cmd_split[len(cmd_split) - 1] == 'sudo' and owner_account_type != 'dev':
        return True

    if user.account_type != 'dev' and owner_account_type == 'dev':
        print("You need developer privileges to access another dev's directory. ")
        return False

    if user.account_type not in ['admin', 'dev'] and owner != user.name:
        print("You need administrator privileges to access another user's directory. ")
        return False


def validate_file_access(directory, filename, user):
    if filename in ChaOS_constants.SYSTEN_FILE_NAMES and user.account_type != 'dev':
        print('You need developer privileges to access a system file or directory. ')
        return False
    else:
        return True


def validate_file_alteration(filename, user):
    if filename in ChaOS_constants.SYSTEN_FILE_NAMES and user.account_type != 'dev':
        print('You need developer privileges to alter a system file. ')


def validate_dir_alteration(dirname, user):
    if dirname in ChaOS_constants.SYSTEM_DIR_NAMES and user.account_type != 'dev':
        print('You need developer privileges to alter a system directory. ')
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
