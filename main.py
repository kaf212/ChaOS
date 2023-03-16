import os
import time
from file import *
from login import login, create_user_ui
from ChaOS_DevTools import *
from system import *
from user import edit_user, delete_user_safe
import platform

import logging
from colors import *

user = login()
cr_dir = f'A/ChaOS_Users/{user.name}'  # cr_dir = the actual current directory: A/ChaOS_Users


def main():
    initialize_user_directories()
    reset_syslog()
    os.system('cls')
    command_prompt()


def command_prompt():
    global user
    global cr_dir
    cr_dir_ui = translate_path_2_ui(cr_dir)  # cr_dir_ui = the simulated directory seen by the user = A:/Users
    while True:
        logging.basicConfig(level='debug', format=ChaOS_constants.LOGGING_FORMAT)
        cmd = input(f'{cr_dir_ui}>')

        cmd_invalid = False
        cmd_split = None
        if cmd:
            try:
                cmd_split = cmd.split()  # splits the input command string into a list, the delimiter is a whitespace.
            except TypeError:
                cmd_invalid = True

            try:
                if cmd_split[0] == 'sudo':
                    cmd_split.remove('sudo')
                    cmd_split.append('')
                    cmd_split.append('')   # yes, this is part 1 of the fix for issue #13
                    cmd_split.append('')
                    cmd_split.append('sudo')
            except IndexError:
                pass

        if not cmd_invalid and cmd != '':
            syslog('command', f'used command "{cmd}"')
            cmd_split = translate_command(cmd_split)
            try:
                if cmd_split[0] == 'create':
                    create_x(cmd_split)

                elif cmd_split[0] == 'read':
                    read_x(cmd_split)

                elif cmd_split[0] == 'delete':
                    delete_x(cmd_split)

                elif cmd_split[0] == 'burn':
                    burn_x(cmd_split)

                elif cmd_split[0] == 'edit':
                    edit_x(cmd_split)

                elif cmd_split[0] == 'cd':
                    dir_cd = change_dir(translate_ui_2_path(cmd_split[1]),
                                        cr_dir, cmd_split)
                    # before a dir change, the user input dir needs to be translated from ui_dir to actual dir.
                    if dir_cd is not None:  # if cd didn't fail
                        cr_dir = dir_cd
                        cr_dir_ui = translate_path_2_ui(cr_dir)

                elif cmd_split[0] == 'dir':
                    list_dir(cr_dir)

                elif cmd_split[0] == 'echo':
                    try:
                        print(cmd_split[1])
                    except IndexError:
                        print_warning('You must enter a valid statement to echo. ')

                elif cmd_split[0] == 'clear':
                    os.system('cls')

                elif cmd_split[0] == 'help':
                    help_cmd(cmd_split)

                elif cmd_split[0] == 'shutdown':
                    shutdown(cmd_split)
                elif cmd_split[0] == 'logoff':
                    user = login()
                    cr_dir = f'A/ChaOS_Users/{user.name}'
                    main()

                elif cmd_split[0] == 'whoami':
                    display_usr(cmd_split)
                elif cmd_split[0] == 'syslog':
                    show_syslog()

                elif cmd_split[0] == 'dev':
                    if user.account_type == 'dev':
                        access_dev_tools(cmd_split)
                    else:
                        print_warning('You need developer privileges to access the DevTools. ')

                else:
                    print_warning(f'The command "{cmd_split[0]}" does not exist. \n')

            except TypeError:
                print_warning('TypeError: You must enter a valid command to proceed, type "help" for help. ')
            except IndexError:
                print_warning('IndexError: You must enter a valid command to proceed, type "help" for help. ')


def help_cmd(cmd_split: list):
    """
    I think this is self-explanatory:
    takes cmd_split as an argument and goes through the dictionary beneath and lists
    the command usage.
    :param cmd_split:
    :return None:
    """
    cmd_usage = {'create': 'create <object> <name>',
                 'read': 'read <object> <name>',
                 'delete': 'delete <object> <name>',
                 'edit': 'edit  <object> <name>',
                 'cd': 'cd <target dir>',
                 'echo': 'echo <string>',
                 'help': 'help <target cmd>',
                 'shutdown': 'shutdown t- <seconds>'
                 }
    try:
        if cmd_split[1] in cmd_usage.keys():
            print(f'-- Help for command {cmd_split[1]} -- ')
            print(f'{cmd_split[1]}: {cmd_usage[cmd_split[1]]}')
    except KeyError:
        print(f'The command "{cmd_split[1]}" does not exist. ')
    except IndexError:
        for cmd, usage in cmd_usage.items():
            print(f'{cmd}: {usage}')


def create_x(cmd_split: list):
    logging.basicConfig(format=ChaOS_constants.LOGGING_FORMAT, level=logging.DEBUG)
    """
    The top-level command interpreter for anything starting with "create".
    :param cmd_split:
    :return None:   
    """
    try:
        if cmd_split[2] == 'sudo':
            print_warning(f'You must enter a valid {cmd_split[1]}name to proceed. ')
            # check if the user didn't forget the name and "sudo" is misinterpreted as the name.
    except IndexError:
        pass

    if cmd_split[1] == 'file':
        if validate_filetype(cmd_split[2], ['.txt']):   # if the file is a txt:
            if not check_file_existence(cr_dir + cmd_split[2]):   # if the file doesn't exist yet:
                create_file(cr_dir, cmd_split[2], user)
            else:
                print_warning(f'The file "{cmd_split[2]}" already exists. ')
    elif cmd_split[1] == 'dir':
        if cmd_split[-1] == 'all_users':
            dir_type = 'communist'
        else:
            dir_type = 'capitalist'
        create_dir(user=user, dir=cr_dir, name=cmd_split[2], cmd_split=cmd_split, dir_type=dir_type)
    elif cmd_split[1] == 'user':
        create_user_ui(user, cmd_split)
        # the difference between create_user() and create_user_ui() is,
        # that the latter prompts for user info in the console.
    else:
        print_warning(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}"\n')


def read_x(cmd_split):
    """
    The top-level command interpreter for anything starting with "read".
    Currently only works for txts.
    :param cmd_split:
    :return None:
    """
    if os.path.isfile(f'{cr_dir}/{cmd_split[2]}'):
        if cmd_split[1] == 'file':
            if cmd_split[2].endswith('.txt'):
                read_txt(cr_dir, cmd_split[2])
            else:
                print_warning(f'"{"." + cmd_split[2].partition(".")[2]}" is not a valid filetype\n')
                # extracts the filetype from the file with the .partition method and "." as delimiter.
        else:
            print_warning(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}\n')
    else:
        print_warning(f'The file "{cr_dir}/{cmd_split[2]}" does not exist. ')


def delete_x(cmd_split):
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
    """
    The top-level command interpreter for anything starting with "delete".
    Currently only works for txts.
    :param cmd_split:
    :return None:
    """
    if cmd_split[2] == 'sudo':
        print_warning(f'You must enter a valid {cmd_split[1]}name to proceed. ')
    # check if the user didn't forget the name and "sudo" is misinterpreted as the name.

    else:
        if cmd_split[1] == 'file':
            if check_file_existence(cr_dir + "/" + cmd_split[2]):
                if validate_file_alteration(cmd_split[2], user):   # make sure the user isn't deleting any system files
                    # delete_file_ui(cr_dir + "/" + cmd_split[2])
                    recycle(cmd_split[2], cr_dir)
                else:
                    pass

        elif cmd_split[1] == 'user':
            delete_user_safe(user, cmd_split[2])

        elif cmd_split[1] == 'dir':
            target_dir = translate_ui_2_path(cmd_split[2])
            if os.path.isdir(cr_dir + '/' + target_dir):
                if validate_dir_access(cmd_split=cmd_split, user=user, dirname=target_dir, parent_dir=cr_dir):
                    # make sure he has access permission
                    if validate_dir_alteration(target_dir, user):   # make sure he's not deleting a system directory
                        recycle(target_dir, cr_dir)
                        # delete_dir_ui(cr_dir, target_dir)
            else:
                print_warning(f'The directory "{cmd_split[2]}" does not exist. ')
        else:
            print_warning(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}"\n')


def burn_x(cmd_split):
    """
    Contrary to deleting, burning just removes the contents of a target and doesn't delete it entirely.
    :param cmd_split:
    :return:
    """
    if os.path.isdir(f'{cr_dir}/{cmd_split[1]}'):
        if validate_dir_access(cr_dir, cmd_split[1], user, cmd_split):
            if cmd_split[1] == 'Recycling bin':
                burn_dir(f'{cr_dir}/Recycling bin')
                print_success(f'Burned "{cmd_split[1]}" successfully. ')
    else:
        print_warning(f'"{cmd_split[1]}" is not a directory. ')


def edit_x(cmd_split):
    """
    The top-level command interpreter dor anything starting with "edit".
    Supports both txts and users.
    :param cmd_split:
    :return None:
    """

    if cmd_split[2] == 'sudo':
        print_warning(f'You must enter a valid {cmd_split[1]}name to proceed. ')
    # check if the user didn't forget the name and "sudo" is misinterpreted as the name.

    else:

        if cmd_split[1] == 'file':
            if check_file_existence(cr_dir + "/" + cmd_split[2]):
                if validate_filetype(cmd_split[2], ['.txt']):
                    edit_txt(cr_dir + "/" + cmd_split[2])
            else:
                print_warning(f'File "{cmd_split[2]}" does not exist. ')

        elif cmd_split[1] == 'user':
            if cmd_split[len(cmd_split) - 1] == 'sudo':
                edit_user(cmd_split)
            elif cmd_split[2] != user.name and user.account_type not in ['admin', 'dev']:
                print_warning('You need administrator privileges to edit another user. ')
            else:
                edit_user(cmd_split)


def change_dir(path, cr_dir, cmd_split):
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
    if path == '..':
        pth_spl = split_path(cr_dir)  # split the current directory into a list
        pth_spl.pop()    # remove the last directory
        pth_spl.pop()    # remove the "/"
        dir = ''.join(pth_spl)  # reconvert it into a string
        return dir

    path_valid = True
    invalid_paths = ['...', '/', '.']
    if path in invalid_paths:
        path_valid = False

    if path_valid:

        if os.path.isdir(path):
            return path

        if not cr_dir.endswith('/'):
            full_path = cr_dir + '/' + path
        else:
            full_path = cr_dir + path

        if os.path.exists(full_path):
            dir = full_path
            if validate_dir_access(parent_dir=cr_dir, user=user, cmd_split=cmd_split, dirname=path):
                return dir
        elif os.path.exists(path):
            dir = path
            if validate_dir_access(parent_dir=cr_dir, user=user, cmd_split=cmd_split, dirname=path):
                # TODO if something's broken, check these arguments for corectness
                return dir
            return dir
        else:
            print_warning(f'The directory "{translate_path_2_ui(path)}" does not exist. ')

    else:
        print_warning(f'The directory "{translate_path_2_ui(path)}" does not exist. ')


def list_dir(cr_dir):
    """
    Is called when cmd "dir" is executed.
    Lists every file and subdirectory in a given directory.
    :param cr_dir:
    :return None:
    """
    equivalents = ChaOS_constants.PATH_2_UI_TRANSLATIONS  # the equivalents are the ui_path to actual path translations

    dirs = os.listdir(cr_dir)
    total_dirs = 0
    total_files = 0
    total_files_size = 0
    for dir in dirs:

        last_modified = os.path.getmtime(f'{cr_dir}/{dir}')
        last_modified = time.ctime(last_modified)

        if '.' not in dir:  # if there's no "." in the name, it can only be a directory.
            total_dirs += 1
            if dir in equivalents:
                print(f'{last_modified}\t<DIR>\t{equivalents[dir]}')
                # if there is a translation for the dir (A, ChaOS_Users)
            else:
                print(f'{last_modified}\t<DIR>\t{dir}')
                # if there's no translations --> user directory, so just print the real name

        else:
            total_files += 1
            total_files_size += os.path.getsize(f'{cr_dir}/{dir}')
            if dir in equivalents:
                print(f'{last_modified}\t\t{equivalents[dir]}')
            else:
                print(f'{last_modified}\t\t{dir}')

    if total_files == 1:
        print(f'\t{total_files} file\t\ttotal: {total_files_size} bytes')
    else:
        print(f'\t{total_files} files\t\ttotal: {total_files_size} bytes')

    if total_dirs == 1:
        print(f'\t{total_dirs} directory')
    else:
        print(f'\t{total_dirs} directories')


def shutdown(cmd_split):
    """
    No explanation needed.
    :param cmd_split:
    :return:
    """
    try:
        if 't-' in cmd_split[1]:  # if the user has specified a countdown with "t-"_
            sd_cd = list(cmd_split[1])
            sd_cd.remove('t')
            sd_cd.remove('-')  # remove "t-"
            sd_cd = ''.join(sd_cd)
            time.sleep(int(sd_cd))
            exit()
    except IndexError:
        exit()


def display_usr(cmd_split):
    if cmd_split[len(cmd_split) - 1] == 'sudo':
        print(f"{platform.uname()[1]}/bootleg_administrator")
    else:
        print(f'{platform.uname()[1]}/{user.name}')


def access_dev_tools(cmd_split):
    """
    The gateway to the land of dangerous and user-unfriendly operations.
    :param cmd_split:
    :return:
    """
    def print_dev(output: str, color=None):   # every output related to the devtools should be recognized as one
        if color is not None:
            if color == 'red':
                print_warning(f'[DEVTOOL]: {output}')
            elif color == 'green':
                print_success(f'[DEVTOOL]: {output}')
            else:
                print(f'[DEVTOOL]: {output}')
        else:
            print(f'[DEVTOOL]: {output}')

    if cmd_split[1] == 'reset':
        if cmd_split[2] == 'user_csv' or cmd_split[2] == 'users_csv':
            try:
                if cmd_split[3] == '-hard':
                    reset_user_csv('-hard')
            except IndexError:
                reset_user_csv(None)
            try:
                if cmd_split[3] == '-hard':
                    print_dev('User CSV was reset HARD successfully. ', 'green')
            except IndexError:
                print_dev('User CSV was reset successfully. ', 'green')

        elif cmd_split[2] == 'user_dirs':
            try:
                if cmd_split[3] == '-hard':
                    reset_user_dirs('-hard')
                    print_dev('User directories were reset HARD successfully. ', 'green')
            except IndexError:
                reset_user_dirs()
                print_dev('User directories were reset successfully. ', 'green')
    else:
        print_dev(f'"{cmd_split[1]}" is not a valid dev command. ', 'red')


def translate_command(cmd_split: list) -> list:
    for item in cmd_split:
        if item in ChaOS_constants.CMD_SHORTS.keys():
            cmd_split[cmd_split.index(item)] = ChaOS_constants.CMD_SHORTS[item]

    try:
        if cmd_split[1] in ['f', 'file']:
            if '.' not in cmd_split[2]:   # when filetype is not specified, change it to .txt
                cmd_split[2] += '.txt'
    except IndexError:
        pass

    return cmd_split


if __name__ == '__main__':
    main()
