import datetime
import os
import time

from file import initialize_user_directories, create_file, read_txt, validate_filetype, check_file_existence, \
    delete_file, edit_txt, create_dir, validate_dir_access
from input import input_y_n
from login import login


def main():
    global ChaOS_version
    ChaOS_version = '1.0.0 Beta'

    initialize_user_directories()
    global user
    user = login()

    global dir_owners
    dir_owners = {'A/ChaOS_Users/kaf221122': 'kaf221122',
                  'A/ChaOS_Users/NexToNothing': 'NexToNothing',
                  'A/ChaOS_Users/Custoomer31': 'Custoomer31',
                  'A/ChaOS_Users/Seve': 'Seve',
                  'A/ChaOS_Users/Manu': 'Manu',
                  'A/ChaOS_Users': 'all users',
                  'A/': 'all users',
                  'A': 'all users',
                  }

    command_prompt()


def command_prompt():
    global cr_dir
    cr_dir = f'A/ChaOS_Users/{user.name}'
    cr_dir_ui = translate_dir_2_ui(cr_dir)
    while True:
        cmd = input(f'{cr_dir_ui}>')

        cmd_invalid = False
        cmd_split = None
        if cmd:
            try:
                cmd_split = cmd.split()
            except TypeError:
                cmd_invalid = True

        if not cmd_invalid:
            try:
                if cmd_split[0] == 'create':
                    create_x(cmd_split)

                elif cmd_split[0] == 'read':
                    read_x(cmd_split)

                elif cmd_split[0] == 'delete':
                    delete_x(cmd_split)

                elif cmd_split[0] == 'edit':
                    edit_x(cmd_split)

                elif cmd_split[0] == 'cd':
                    dir_cd = change_dir(translate_ui_2_dir(cmd_split[1]), cr_dir)
                    if dir_cd is not None:  # if cd didn't fail
                        cr_dir = dir_cd
                        cr_dir_ui = translate_dir_2_ui(cr_dir)

                elif cmd_split[0] == 'dir':
                    list_dir(cr_dir)

                elif cmd_split[0] == 'shutdown':
                    shutdown(cmd_split)

                else:
                    print(f'The command "{cmd_split[0]}" does not exist. \n')

            except TypeError:
                print('You must enter a valid command to proceed, type "help" for help. ')
            except IndexError:
                print('You must enter a valid command to proceed, type "help" for help. ')


def create_x(cmd_split):
    if cmd_split[1] == 'file':
        if validate_filetype(cmd_split[2], ['.txt']):
            if not check_file_existence(cr_dir + cmd_split[2]):
                create_file(cr_dir, cmd_split[2], user, ChaOS_version)
            else:
                print(f'The file "{cmd_split[2]}" already exists. ')

    elif cmd_split[1] == 'dir':
        create_dir(cr_dir, cmd_split[2])

    elif cmd_split[1] == 'user':
        pass
    else:
        print(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}"\n')


def read_x(cmd_split):
    if cmd_split[1] == 'file':
        if cmd_split[2].endswith('.txt'):
            read_txt(cr_dir, cmd_split[2])
        else:
            print(f'"{"." + cmd_split[2].partition(".")[2]}" is not a valid filetype\n')
    else:
        print(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}\n')


def delete_x(cmd_split):
    if cmd_split[1] == 'file':
        if check_file_existence(cr_dir + "/" + cmd_split[2]):
            confirmation = input_y_n(f'Delete {cr_dir + "/" + cmd_split[2]}? > ')
            if confirmation == 'y':
                delete_file(cr_dir + "/" + cmd_split[2])
                print(f'Deleted {cmd_split[2]}')
            else:
                pass

    elif cmd_split[1] == 'user':
        pass
    else:
        print(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}"\n')


def edit_x(cmd_split):
    if cmd_split[1] == 'file':
        if check_file_existence(cr_dir + "/" + cmd_split[2]):
            if validate_filetype(cmd_split[2], ['.txt']):
                edit_txt(cr_dir + "/" + cmd_split[2])
        else:
            print(f'File "{cmd_split[2]}" does not exist. ')


def change_dir(path, cr_dir):
    if not cr_dir.endswith('/'):
        full_path = cr_dir + '/' + path
    else:
        full_path = cr_dir + path

    print(f'DEBUGGING: full_path = {full_path}')
    print(f'DEBUGGING: path = {path}')

    if os.path.exists(full_path):
        dir = full_path
        if validate_dir_access(dir, dir_owners, user):
            return dir
        else:
            print(f"You don't have access permission to {dir}")
    elif os.path.exists(path):
        dir = path
        if validate_dir_access(dir, dir_owners, user):
            return dir
        else:
            print(f"You don't have access permission to {dir}")
        return dir
    else:
        print(f'The directory "{path}" does not exist. ')


def list_dir(cr_dir):
    equivalents = {'A': 'A:',
                   'ChaOS_Users': 'Users',
                   }

    dirs = os.listdir(cr_dir)
    for dir in dirs:
        if '.' not in dir:
            if dir in equivalents:
                print(f'<DIR>\t{equivalents[dir]}')
            else:
                print(f'<DIR>\t{dir}')

        else:
            if dir in equivalents:
                print(f'\t\t{equivalents[dir]}')
            else:
                print(f'\t\t{dir}')


def translate_dir_2_ui(cr_dir):
    equivalents = {'A': 'A:',
                   'ChaOS_Users': 'Users',
                   }

    cr_dir_split = split_path(cr_dir)

    ui_dir_list = []

    for dir in cr_dir_split:
        if dir in equivalents.keys():
            dir = equivalents[dir]
        ui_dir_list.append(dir)

    ui_dir = ''.join(ui_dir_list)

    return ui_dir


def translate_ui_2_dir(ui_dir):
    equivalents = {'A:': 'A',
                   'Users': 'ChaOS_Users',
                   }

    ui_dir_split = split_path(ui_dir)

    dir_list = []

    for dir in ui_dir_split:
        if dir in equivalents.keys():
            dir = equivalents[dir]
        dir_list.append(dir)

    dir = ''.join(dir_list)

    return dir


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


def shutdown(cmd_split):
    try:
        if 't-' in cmd_split[1]:
            sd_cd = list(cmd_split[1])
            sd_cd.remove('t')
            sd_cd.remove('-')
            sd_cd = ''.join(sd_cd)
            time.sleep(int(sd_cd))
            exit()
    except IndexError:
        exit()


if __name__ == '__main__':
    main()
