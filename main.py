import socket
import time

import cmd_definitions
from file import *
from login import login, create_user_ui
from ChaOS_DevTools import *
from system import *
from user import edit_user, delete_user_safe
from cmd_definitions import cmd_def_map, cmd_usage
import platform
from dataclasses import dataclass, field
from ChaOS_constants import CMD_SHORTS

import logging
from colors import *


@dataclass
class Cmd:
    cmd: str = None
    pri_arg: str = None
    sec_arg: str = None
    ter_arg: str = None
    flags: dict = field(default_factory=dict)
    perm_arg: str = None

    def interpret(self, cmd_str: str):
        cmd_split = cmd_str.split()
        try:
            self.cmd = cmd_split[0]
        except IndexError:
            print('You must enter a valid command to interact with the system. ')
        try:
            self.pri_arg = cmd_split[1]
            self.sec_arg = cmd_split[2]
            self.ter_arg = cmd_split[3]
            # self.flags = cmd_split[4]  # TODO: add support for flags
            self.perm_arg = cmd_split[-1]
        except IndexError:
            pass

        for arg in cmd_split:
            if arg.startswith('-'):
                self.flags[arg] = cmd_split[cmd_split.index(arg) + 1]

    def compile(self):
        if self.cmd in CMD_SHORTS.keys():  # compile the command from keyword to cmd
            self.cmd = CMD_SHORTS[self.cmd]
        if self.pri_arg in CMD_SHORTS.keys():  # compile the primary argument from keyword to cmd (for help cmd)
            self.pri_arg = CMD_SHORTS[self.pri_arg]

        for attr, value in self.__dict__.items():
            if type(value) == str and (not value.startswith('__') and '/' in value):  # loop over all attributes and if they're
                # not a builtin and are a path, translate them
                self.__dict__[attr] = translate_ui_2_path(value)
            if value == 'sudo':
                self.perm_arg = 'sudo'
                self.__dict__[attr] = None

    def validate(self):
        if self.cmd not in cmd_map:
            print_warning(f'The command "{self.cmd}" does not exist. ')
            return False
        try:
            if self.pri_arg not in cmd_vld_arg_map[self.cmd]:
                print_warning(f'"{self.pri_arg}" is not a valid statement for command "{self.cmd}". ')
                return False
        except KeyError:
            pass
        return True

    def execute(self):
        if self.cmd in cmd_map.keys():
            try:
                args = cmd_args_map[self.cmd]
            except KeyError:  # if the function doesn't take any arguments
                args = []

            func = cmd_map[self.cmd]
            func(*args)
        else:
            print_warning(f'Command not found in cmd_map (Add support for non cmd_map commands!). ')
            # TODO: add support for commands not in cmd_map


user = login()
cr_dir = f'A/ChaOS_Users/{user.name}'  # cr_dir = the actual current directory: A/ChaOS_Users
cmd_split = []
cmd_obj = Cmd()
print(hex(id(cmd_obj)))


def main():
    initialize_user_directories()
    reset_syslog()
    os.system('cls')
    command_prompt()


def command_prompt():
    global cmd_split
    global user
    global cr_dir
    global cmd_obj
    cr_dir_ui = translate_path_2_ui(cr_dir)  # cr_dir_ui = the simulated directory seen by the user = A:/Users
    while True:
        logging.basicConfig(level='debug', format=ChaOS_constants.LOGGING_FORMAT)
        cmd_str = input(f'{cr_dir_ui}>')

        if cmd_str:
            cmd_obj.interpret(cmd_str)
            cmd_obj.compile()
            if cmd_obj.validate():
                cmd_obj.execute()

        #    else:
        #        try:
#
        #            if cmd_split[0] == 'cd':
        #                dir_cd = change_dir(translate_ui_2_path(cmd_split[1]),
        #                                    cr_dir, cmd_split)
        #                # before a dir change, the user input dir needs to be translated from ui_dir to actual dir.
        #                if dir_cd is not None:  # if cd didn't fail
        #                    cr_dir = dir_cd
        #                    cr_dir_ui = translate_path_2_ui(cr_dir)
#
        #            elif cmd_split[0] == 'logoff':
        #                user = login()
        #                cr_dir = f'A/ChaOS_Users/{user.name}'
        #                main()
#
        #            elif cmd_split[0] == 'dev':
        #                if user.account_type == 'dev':
        #                    access_dev_tools(cmd_split)
        #                else:
        #                    print_warning('You need developer privileges to access the DevTools. ')
#
        #            else:
        #                print_warning(f'The command "{cmd_split[0]}" does not exist. \n')
#
        #        except TypeError:
        #            print_warning('TypeError: You must enter a valid command to proceed, type "help" for help. ')
        #        except IndexError:
        #            print_warning('IndexError: You must enter a valid command to proceed, type "help" for help. ')


def help_cmd(cmd):
    """
    I think this is self-explanatory:
    takes cmd_split as an argument and goes through the dictionary beneath and lists
    the command usage.
    :param cmd:
    :return None:
    """
    print(hex(id(cmd)))
    try:
        if cmd.pri_arg in cmd_usage.keys():
            print(f'-- Help for command {cmd.pri_arg} -- ')
            print(f'Syntax: {cmd_usage[cmd.pri_arg]}')
        else:
            print_warning(f'The command "{cmd.pri_arg}" does not exist. ')
            return None
    except IndexError:
        for command, usage in cmd_usage.items():
            print(f'{command}: {usage}')


    # print()
    # if cmd.sec_arg == '-def':
    #     try:
    #         print(cmd_definitions.cmd_def_map[cmd.pri_arg])
    #     except IndexError:
    #         print_warning(f'No definition found for command "{cmd.pri_arg}". ')
    #     except KeyError:
    #         print_warning(f'No definition found for command "{cmd.pri_arg}". ')
    #     print()


def create_x(cmd):
    """
    The top-level command interpreter for anything starting with "create".
    :param cmd_split:
    :return None:
    """
    logging.basicConfig(format=ChaOS_constants.LOGGING_FORMAT, level=logging.DEBUG)

    try:
        if cmd.perm_arg == 'sudo':
            print_warning(f'You must enter a valid {cmd.pri_arg}name to proceed. ')
            # check if the user didn't forget the name and "sudo" is misinterpreted as the name.
    except IndexError:
        pass

    if cmd.pri_arg == 'file':
        if validate_filetype(cmd.sec_arg, ['.txt']):  # if the file is a txt:
            if not check_file_existence(cr_dir + cmd.sec_arg):  # if the file doesn't exist yet:
                create_file(cr_dir, cmd.sec_arg, user)
            else:
                print_warning(f'The file "{cmd.sec_arg}" already exists. ')
    elif cmd.pri_arg == 'dir':
        if cmd_split[-1] == 'all_users':
            dir_type = 'communist'
        else:
            dir_type = 'capitalist'
        create_dir(user=user, dir=cr_dir, name=cmd.sec_arg, cmd_split=cmd_split, dir_type=dir_type)
    elif cmd.pri_arg == 'user':
        create_user_ui(user, cmd_split)
        # the difference between create_user() and create_user_ui() is,
        # that the latter prompts for user info in the console.
    else:
        print_warning(f'"{cmd.pri_arg}" is not a valid statement for command "{cmd.cmd}"\n')


def read_x(cmd):
    """
    The top-level command interpreter for anything starting with "read".
    Currently only works for txts.
    :param cmd_split:
    :return None:
    """
    if not os.path.isfile(f'{cr_dir}/{cmd.sec_arg}'):
        print_warning(f'The file "{cr_dir}/{cmd.sec_arg}" does not exist. ')
        return None

    if cmd.pri_arg != 'file':
        print_warning(f'"{cmd.pri_arg}" is not a valid statement for command "{cmd.cmd}\n')
        return None

    if cmd.sec_arg.endswith('.txt'):
        read_txt(cr_dir, cmd.sec_arg)
    else:
        print_warning(f'"{"." + cmd.sec_arg.partition(".")[2]}" is not a valid filetype\n')
        # extracts the filetype from the file with the .partition method and "." as delimiter.


def delete_x(cmd):
    """
    The top-level command interpreter for anything starting with "delete".
    Currently only works for txts.
    :param cmd_split:
    :return None:
    """
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
    try:
        if cmd.perm_arg == 'sudo':
            print_warning(f'You must enter a valid {cmd.pri_arg}name to proceed. ')
            return None
    except IndexError:
        pass
    # check if the user didn't forget the name and "sudo" is misinterpreted as the name.

    if cmd.pri_arg == 'file':
        if not os.path.isfile(cr_dir + "/" + cmd.sec_arg):
            print_warning(f'The file "{cr_dir + "/" + cmd.sec_arg}" is not a file or does not exist. ')
            return None
        if validate_file_alteration(cmd.sec_arg, user):  # make sure the user isn't deleting any system files
            # delete_file_ui(cr_dir + "/" + cmd.sec_arg)
            recycle(cmd.sec_arg, cr_dir)

    elif cmd.pri_arg == 'user':
        delete_user_safe(user, cmd.sec_arg)

    elif cmd.pri_arg == 'dir':
        target_dir = translate_ui_2_path(cmd.sec_arg)
        if not os.path.isdir(cr_dir + '/' + target_dir):
            print_warning(f'The directory "{cmd.sec_arg}" does not exist. ')
            return None

        if not validate_dir_access(cmd_split=cmd_split, user=user, dirname=target_dir, parent_dir=cr_dir):
            return None

        # make sure he has access permission
        if not validate_dir_alteration(target_dir, user):  # make sure he's not deleting a system directory
            return None

        if target_dir == 'Recycling bin':
            print_warning('You cannot delete the recycling bin. ')
            return None

        if cr_dir in ['A', 'A/ChaOS_Users']:
            delete_dir(target_dir, cr_dir)
        else:
            recycle(target_dir, cr_dir)
            # delete_dir_ui(cr_dir, target_dir)
    else:
        print_warning(f'"{cmd.pri_arg}" is not a valid statement for command "{cmd.cmd}"\n')


def restore_x(cmd):
    rec_bin_dir = f'{cr_dir}/Recycling bin'
    if not os.path.exists(rec_bin_dir):
        print_warning(f'There is no recycling bin in "{translate_path_2_ui(cr_dir)}". ')
        return None  # neat way to just exit the function

    if validate_dir_access(cr_dir, 'Recycling bin', user, cmd_split):
        if cmd.pri_arg == 'file':
            target_path = f'{rec_bin_dir}/{cmd.sec_arg}'
            if os.path.isfile(target_path):
                restore_file(cmd.sec_arg, rec_bin_dir)
            else:
                print_warning(f'The file "{translate_path_2_ui(target_path)}" does not exist. ')

        if cmd.pri_arg == 'dir':
            target_path = f'{rec_bin_dir}/{cmd.sec_arg}'
            if os.path.isdir(target_path):
                print_warning(f'You cannot yet restore directories. ')

            else:
                print_warning(f'The directory "{translate_path_2_ui(target_path)}" does not exist. ')


def burn_x(cmd):
    """
    Contrary to deleting, burning removes data from its pathetic existence with no steps inbetween.
    :param cmd_split:
    :return:
    """
    path = f'{cr_dir}/{cmd.sec_arg}'
    if cmd.pri_arg == 'dir':
        if os.path.isdir(f'{cr_dir}/{cmd.sec_arg}'):
            if validate_dir_access(cr_dir, cmd.sec_arg, user, cmd_split):
                if cmd.sec_arg == 'Recycling bin':
                    if input_y_n(f'Burn recycling bin? > ') == 'y':
                        shutil.rmtree(path)
                        os.mkdir(path)
                        create_md_file(path)
                        syslog('deletion', f'burned recycling bin. ')
                        print_success(f'Burned "{cmd.sec_arg}" successfully. ')
                else:
                    if cmd.sec_arg not in ChaOS_constants.SYSTEM_DIR_NAMES:
                        if input_y_n(f'Burn "{cmd.sec_arg}"? > ') == 'y':
                            shutil.rmtree(path)
                            delete_metadata(cmd.sec_arg, cr_dir)
                            syslog('deletion', f'burned directory "{translate_path_2_ui(path)}". ')
                            print_success(f'Burned "{cmd.sec_arg}" successfully. ')
                    else:
                        print_warning('You cannot burn system directories. ')
    elif cmd.pri_arg == 'file':
        if os.path.isfile(f'{cr_dir}/{cmd.sec_arg}'):
            if cmd.sec_arg not in ChaOS_constants.SYSTEN_FILE_NAMES:
                if input_y_n(f'Burn "{cmd.sec_arg}"? > ') == 'y':
                    os.remove(path)
                    syslog('deletion', f'burned file "{translate_path_2_ui(path)}". ')
                    print_success(f'Burned "{cmd.sec_arg}" successfully. ')
            else:
                print_warning(f'You cannot burn a system file. ')
        else:
            print_warning(f'"{path}" is not a file. ')


def edit_x(cmd):
    """
    The top-level command interpreter dor anything starting with "edit".
    Supports both txts and users.
    :param cmd_split:
    :return None:
    """

    if cmd.perm_arg == 'sudo':
        print_warning(f'You must enter a valid {cmd.pri_arg}name to proceed. ')
    # check if the user didn't forget the name and "sudo" is misinterpreted as the name.

    else:

        if cmd.pri_arg == 'file':
            if check_file_existence(cr_dir + "/" + cmd.sec_arg):
                if validate_filetype(cmd.sec_arg, ['.txt']):
                    edit_txt(cr_dir + "/" + cmd.sec_arg)
            else:
                print_warning(f'File "{cmd.sec_arg}" does not exist. ')

        elif cmd.pri_arg == 'user':
            if cmd_split[len(cmd_split) - 1] == 'sudo':
                edit_user(cmd_split)
            elif cmd.sec_arg != user.name and user.account_type not in ['admin', 'dev']:
                print_warning('You need administrator privileges to edit another user. ')
            else:
                edit_user(cmd_split)


def change_dir(path, cr_dir, cmd):
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
    if path == '..':
        pth_spl = split_path(cr_dir)  # split the current directory into a list
        pth_spl.pop()  # remove the last directory
        pth_spl.pop()  # remove the "/"
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
                print(f'{last_modified}\t\t\t{equivalents[dir]}')
            else:
                print(f'{last_modified}\t\t\t{dir}')

    if total_files == 1:
        print(f'\t{total_files} file\t\ttotal: {total_files_size} bytes')
    else:
        print(f'\t{total_files} files\t\ttotal: {total_files_size} bytes')

    if total_dirs == 1:
        print(f'\t{total_dirs} directory')
    else:
        print(f'\t{total_dirs} directories')


def echo(cmd):
    print_warning(cmd)
    print(cmd.pri_arg)


def clear_screen():
    os.system('cls')


def shutdown(cmd):
    """
    No explanation needed.
    :param cmd_split:
    :return:
    """
    try:
        if 't-' in cmd.pri_arg:  # if the user has specified a countdown with "t-"_
            sd_cd = list(cmd.pri_arg)
            sd_cd.remove('t')
            sd_cd.remove('-')  # remove "t-"
            sd_cd = ''.join(sd_cd)
            time.sleep(int(sd_cd))
            exit()
    except IndexError:
        exit()


def display_usr(cmd):
    if cmd_split[len(cmd_split) - 1] == 'sudo':
        print(f"{platform.uname()[1]}/bootleg_administrator")
    else:
        print(f'{"Username:":15}{user.name}')
        print(f'{"Account type:":15}{user.account_type}')
        print(f'{"Hostname:":15}{platform.uname()[1]}')
        print(f'{"IPv4:":15}{socket.gethostbyname(socket.gethostname())}')


def access_dev_tools(cmd):
    """
    The gateway to the land of dangerous and user-unfriendly operations.
    :param cmd_split:
    :return:
    """

    def print_dev(output: str, color=None):  # every output related to the devtools should be recognized as one
        if color is not None:
            if color == 'red':
                print_warning(f'[DEVTOOL]: {output}')
            elif color == 'green':
                print_success(f'[DEVTOOL]: {output}')
            else:
                print(f'[DEVTOOL]: {output}')
        else:
            print(f'[DEVTOOL]: {output}')

    if cmd.pri_arg == 'reset':
        if cmd.sec_arg == 'user_csv' or cmd.sec_arg == 'users_csv':
            try:
                if cmd.ter_arg == '-hard':
                    reset_user_csv('-hard')
            except IndexError:
                reset_user_csv(None)
            try:
                if cmd.ter_arg == '-hard':
                    print_dev('User CSV was reset HARD successfully. ', 'green')
            except IndexError:
                print_dev('User CSV was reset successfully. ', 'green')

        elif cmd.sec_arg == 'user_dirs':
            try:
                if cmd.ter_arg == '-hard':
                    reset_user_dirs('-hard')
                    print_dev('User directories were reset HARD successfully. ', 'green')
            except IndexError:
                reset_user_dirs()
                print_dev('User directories were reset successfully. ', 'green')
    else:
        print_dev(f'"{cmd.pri_arg}" is not a valid dev command. ', 'red')


cmd_map = {'create': create_x,
           'read': read_x,
           'delete': delete_x,
           'burn': burn_x,
           'restore': restore_x,
           'edit': edit_x,
           'dir': list_dir,
           'echo': echo,
           'clear': clear_screen,
           'help': help_cmd,
           'shutdown': shutdown,
           'whoami': display_usr,
           'syslog': show_syslog,
           'ipconfig': display_ipconfig,
           'move': move_file,
           'dev': access_dev_tools
           }

cmd_args_map = {'create': [cmd_obj],
                'read': [cmd_obj],
                'delete': [cmd_obj],
                'burn': [cmd_obj],
                'restore': [cmd_obj],
                'edit': [cmd_obj],
                'dir': [cr_dir],
                'echo': [cmd_obj],
                'help': [cmd_obj],
                'shutdown': [cmd_obj],
                'whoami': [cmd_obj],
                'ipconfig': [cmd_obj],
                'move': [cr_dir, user, cmd_obj],
                'dev': [cmd_obj]
                }

cmd_vld_arg_map = {'create': ['file', 'dir', 'user'],
                   'read': ['file'],
                   'delete': ['file', 'dir', 'user'],
                   'burn': ['file', 'dir'],
                   'restore': ['file', 'dir'],
                   'edit': ['file', 'user'],
                   'dev': ['reset'],
                   'ipconfig': ['all'],
                   'move': ['file', 'dir']
                   }

if __name__ == '__main__':
    main()
