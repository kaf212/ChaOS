import socket
import time

import cmd_definitions
from TNTFS import File, translate_path_2_ui, translate_ui_2_path, initialize_A_drive, read_txt, \
    reset_user_dirs, split_path
from login import login, create_user_ui
from ChaOS_DevTools import *
from system import *
from user import edit_user, delete_user_safe
from cmd_definitions import cmd_usage
import platform
from dataclasses import dataclass, field
from ChaOS_constants import CMD_SHORTS
from ChaOS_pm import pm_install

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
        for arg in cmd_split:
            if arg == 'sudo':
                cmd_split.remove('sudo')
                self.perm_arg = 'sudo'
        try:
            self.cmd = cmd_split[0]
        except IndexError:
            print('You must enter a valid command to interact with the system. ')
        try:
            self.pri_arg = cmd_split[1]
            self.sec_arg = cmd_split[2]
            self.ter_arg = cmd_split[3]
        except IndexError:
            pass

        for arg in cmd_split:
            if arg.startswith('-'):
                try:
                    self.flags[arg] = cmd_split[cmd_split.index(arg) + 1]
                except IndexError:  # if the flag expects no argument (like -def in cmd "help")
                    self.flags[arg] = None

    def compile(self):
        if self.cmd in CMD_SHORTS.keys():  # compile the command from keyword to cmd
            self.cmd = CMD_SHORTS[self.cmd]
        if self.pri_arg in CMD_SHORTS.keys():  # compile the primary argument from keyword to cmd (for help cmd)
            self.pri_arg = CMD_SHORTS[self.pri_arg]

        for attr, value in self.__dict__.items():
            if type(value) == str and (not value.startswith('__') and '/' in value):
                # loop over all attributes and if they're not a builtin and are a path, translate them
                self.__dict__[attr] = translate_ui_2_path(value)
        if self.pri_arg == 'file' and '.' not in self.sec_arg:  # automatically adds ".txt" to files with no extension.
            self.sec_arg += '.txt'

    def validate(self):
        if self.cmd not in return_all_commands():
            print_warning(f'The command "{self.cmd}" does not exist. ')
            return False

        vld_args = return_cmd_dict(self.cmd, 'vld_cmd_args')
        if vld_args:
            if self.pri_arg not in vld_args:
                print_warning(f'"{self.pri_arg}" is not a valid statement for command "{self.cmd}". ')
                return False
        return True

    """
    def execute(self):
        if self.cmd in cmd_map.keys():
            try:
                args = cmd_args_map[self.cmd]
            except KeyError:  # if the function doesn't take any arguments
                args = []

            func = cmd_map[self.cmd]
            func(*args)
            print_warning(f'executed command: {cmd_obj}')
        else:
            print_warning(f'Command not found in cmd_map (Add support for non cmd_map commands!). ')
            # TODO: add support for commands not in cmd_map
    """

    def execute(self):
        for cmd_dict in cmd_map:
            if cmd_dict['cmd'] == self.cmd:
                func = cmd_dict['func']
                try:
                    args = cmd_dict['args']
                except KeyError:
                    args = []

                func(*args)

    def reset(self):
        for attr, value in self.__dict__.items():
            if type(value) == str and not value.startswith('__'):
                self.__dict__[attr] = None
            elif type(value) == dict:
                self.__dict__[attr] = dict()

    def flag_exists(self, flag):
        for key in self.flags.keys():
            if key == flag:
                return True
        return False

    def get_flag(self, flag):
        for key, value in self.flags.items():
            if key == flag:
                return value
        return None


user = login()
cr_dir = f'A/ChaOS_Users/{user.name}'  # cr_dir = the actual current directory: A/ChaOS_Users
cmd_obj = Cmd()


def main():
    initialize_A_drive()
    reset_syslog()
    os.system('cls')
    command_prompt()


def command_prompt():
    global user
    global cr_dir
    global cmd_obj
    while True:
        cmd_str = input(f'{translate_path_2_ui(cr_dir)}>')
        cmd_obj.reset()
        if cmd_str:
            cmd_obj.interpret(cmd_str)
            cmd_obj.compile()
            if cmd_obj.validate():
                cmd_obj.execute()


def help_cmd(cmd):
    """
    I think this is self-explanatory:
    takes the cmd as an argument and goes through the dictionary beneath and lists
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

    print()
    if '-def' in cmd.flags.keys():
        try:
            print(cmd_definitions.cmd_def_map[cmd.pri_arg])
        except IndexError:
            print_warning(f'No definition found for command "{cmd.pri_arg}". ')
        except KeyError:
            print_warning(f'No definition found for command "{cmd.pri_arg}". ')
        print()


def create_x(cmd):
    if cmd.pri_arg == 'file':
        file = File()
        file.init(cmd, user, cr_dir)
        if file.validate(valid_filetypes=['txt']):
            file.log_metadata()
            file.create_phys()
        del file

    if cmd.pri_arg == 'dir':
        directory = File()
        directory.init(cmd, user, cr_dir)
        if directory.validate():
            directory.log_metadata()
            directory.create_phys()
        del directory

    if cmd.pri_arg == 'user':
        create_user_ui(user, cmd)


def read_x(cmd):
    """
    The top-level command interpreter for anything starting with "read".
    Currently only works for txts.
    :param cmd:
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
    if cmd.pri_arg in ['file', 'dir']:
        file = File()
        file.init(cmd, user, cr_dir)
        file.create_phys()
        del file
    if cmd.pri_arg == 'user':
        delete_user_safe(user, cmd.sec_arg)


def restore_x(cmd):
    rec_bin_dir = f'{cr_dir}/Recycling bin'
    if not os.path.exists(rec_bin_dir):
        print_warning(f'There is no recycling bin in "{translate_path_2_ui(cr_dir)}". ')
        return None  # neat way to just exit the function

    file = File()
    file.select(cmd.sec_arg, rec_bin_dir)
    if file.validate_access(user):
        file.restore(cr_dir)


def move_x(cmd):
    file = File()
    file.select(cmd.sec_arg, cr_dir)
    if file.validate_access(user):
        file.move(cmd.ter_arg)


def burn_x(cmd):
    if cmd.pri_arg in ['file', 'dir']:
        file = File()
        file.select(cmd.sec_arg, cr_dir)
        file.delete()
        del file

    if cmd.pri_arg == 'user':
        delete_user_safe(user, cmd.sec_arg)


def edit_x(cmd):
    if cmd.perm_arg == 'sudo':
        print_warning(f'You must enter a valid {cmd.pri_arg}name to proceed. ')
        return None
    # check if the user didn't forget the name and "sudo" is misinterpreted as the name.

    if cmd.pri_arg == 'file':
        file = File()
        file.select(cmd.sec_arg, cr_dir)
        if file.validate_access(user):
            file.edit_ui()
    elif cmd.pri_arg == 'user':
        if cmd.perm_arg == 'sudo':
            edit_user(cmd)
        elif cmd.sec_arg != user.name and user.account_type not in ['admin', 'dev']:
            print_warning('You need administrator privileges to edit another user. ')
        else:
            edit_user(cmd)


def change_dir(cmd):
    global cr_dir
    path = cmd.pri_arg
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
    if path == '..':
        print_warning(cr_dir)
        pth_spl = split_path(cr_dir)  # split the current directory into a list
        pth_spl.pop()  # remove the last directory
        pth_spl.pop()  # remove the "/"
        cr_dir = ''.join(pth_spl)  # reconvert it into a string
        print_warning(f'cr_dir = {cr_dir}')
        return None

    path_valid = True
    invalid_paths = ['...', '/', '.']
    if path in invalid_paths:
        path_valid = False

    if path_valid:
        if os.path.isdir(path):
            cr_dir = path

        if not cr_dir.endswith('/'):
            full_path = cr_dir + '/' + path
        else:
            full_path = cr_dir + path

        full_path = translate_ui_2_path(full_path)
        path = translate_ui_2_path(path)

        if os.path.exists(full_path):
            dir_obj = File()
            dir_obj.select(full_path, cr_dir)
            if dir_obj.validate_access(user):
                cr_dir = full_path
                return None
        elif os.path.exists(path):
            dir_obj = File()
            dir_obj.select(path, cr_dir)
            if dir_obj.validate_access(user):
                cr_dir = path
                return None
            cr_dir = full_path
            return None
        else:
            print_warning(f'The directory "{translate_path_2_ui(path)}" does not exist. ')

    else:
        print_warning(f'The directory "{translate_path_2_ui(path)}" does not exist. ')


def list_dir():
    """
    Is called when cmd "dir" is executed.
    Lists every file and subdirectory in a given directory.
    :return None:
    """
    global cr_dir
    equivalents = ChaOS_constants.PATH_2_UI_TRANSLATIONS  # the equivalents are the ui_path to actual path translations

    dirs = os.listdir(cr_dir)
    total_dirs = 0
    total_files = 0
    total_files_size = 0
    for directory in dirs:

        last_modified = os.path.getmtime(f'{cr_dir}/{directory}')
        last_modified = time.ctime(last_modified)

        if '.' not in directory:  # if there's no "." in the name, it can only be a directory.
            total_dirs += 1
            if directory in equivalents:
                print(f'{last_modified}\t<DIR>\t{equivalents[directory]}')
                # if there is a translation for the dir (A, ChaOS_Users)
            else:
                print(f'{last_modified}\t<DIR>\t{directory}')
                # if there's no translations --> user directory, so just print the real name

        else:
            total_files += 1
            total_files_size += os.path.getsize(f'{cr_dir}/{directory}')
            if directory in equivalents:
                print(f'{last_modified}\t\t\t{equivalents[directory]}')
            else:
                print(f'{last_modified}\t\t\t{directory}')

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
    :param cmd:
    :return:
    """
    if cmd.flag_exists('-t'):
        try:
            time.sleep(int(cmd.get_flag('-t')))
        except ValueError:
            print_warning(f'Invalid countdown time given "{cmd.get_flag("-t")}"')
            return None
    exit()


def display_usr(cmd):
    if cmd.perm_arg == 'sudo':
        print(f"{platform.uname()[1]}/bootleg_administrator")
    else:
        print(f'{"Username:":15}{user.name}')
        print(f'{"Account type:":15}{user.account_type}')
        print(f'{"Hostname:":15}{platform.uname()[1]}')
        print(f'{"IPv4:":15}{socket.gethostbyname(socket.gethostname())}')


def logoff():
    global cr_dir
    global user
    user = login()
    cr_dir = f'A/ChaOS_Users/{user.name}'
    main()


def access_pm(cmd):
    if cmd.pri_arg == 'install':
        pm_install(cmd)


def run_program(cmd):
    program_name = cmd.pri_arg
    if program_name not in os.listdir('A/System42/programs'):
        print_warning(f'The program "{program_name}" is not installed. ')
        return None

    module_name = f"A.System42.programs.{program_name}.{program_name}_main"
    function_name = f'{program_name}_main'

    impmodule = __import__(module_name, fromlist=[function_name])
    func = getattr(impmodule, function_name)
    func()
    return None


def access_dev_tools(cmd):
    """
    The gateway to the land of dangerous and user-unfriendly operations.
    :param cmd:
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

    if user.account_type != 'dev':
        print_warning('You need developer privileges to access the DevTools. ')
        return None

    if cmd.pri_arg == 'reset':
        if cmd.sec_arg == 'user_csv' or cmd.sec_arg == 'users_csv':
            if cmd.flag_exists('-hard'):
                reset_user_csv('-hard')
                print_dev('User CSV was reset HARD successfully. ', 'green')
            else:
                reset_user_csv(None)
                print_dev('User CSV was reset successfully. ', 'green')

        elif cmd.sec_arg == 'user_dirs':
            if cmd.flag_exists('-hard'):
                reset_user_dirs('-hard')
                print_dev('User directories were reset HARD successfully. ', 'green')
            else:
                reset_user_dirs()
                print_dev('User directories were reset successfully. ', 'green')
    else:
        print_dev(f'"{cmd.pri_arg}" is not a valid dev command. ', 'red')


def return_cmd_dict(trg: str, key: str = None):
    for cmd_dict in cmd_map:
        if cmd_dict['cmd'] == trg:
            if key:
                try:
                    return cmd_dict[key]
                except (KeyError, TypeError):
                    return None
            else:
                return cmd_dict


def return_all_commands():
    all_cmds = []
    for cmd_dict in cmd_map:
        all_cmds.append(cmd_dict['cmd'])
    return all_cmds


cmd_map = [
               {'cmd': 'create', 'func': create_x, 'args': [cmd_obj], 'vld_cmd_args': ['file', 'dir', 'user']},
               {'cmd': 'read', 'func': read_x, 'args': [cmd_obj], 'vld_cmd_args': ['file']},
               {'cmd': 'delete', 'func': delete_x, 'args': [cmd_obj], 'vld_cmd_args': ['file', 'dir', 'user']},
               {'cmd': 'burn', 'func': burn_x, 'args': [cmd_obj], 'vld_cmd_args': ['file', 'dir']},
               {'cmd': 'restore', 'func': restore_x, 'args': [cmd_obj], 'vld_cmd_args': ['file', 'dir']},
               {'cmd': 'edit', 'func': edit_x, 'args': [cmd_obj], 'vld_cmd_args': ['file', 'user']},
               {'cmd': 'dir', 'func': list_dir},
               {'cmd': 'echo', 'func': echo, 'args': [cmd_obj]},
               {'cmd': 'clear', 'func': clear_screen(), 'args': []},
               {'cmd': 'help', 'func': help_cmd, 'args': [cmd_obj]},
               {'cmd': 'shutdown', 'func': shutdown, 'args': [cmd_obj]},
               {'cmd': 'whoami', 'func': display_usr, 'args': [cmd_obj]},
               {'cmd': 'syslog', 'func': show_syslog, 'args': [cmd_obj]},
               {'cmd': 'ipconfig', 'func': display_ipconfig, 'args': [cmd_obj]},
               {'cmd': 'move', 'func': move_x, 'args': [cr_dir, user, cmd_obj], 'vld_cmd_args': ['file', 'dir']},
               {'cmd': 'dev', 'func': access_dev_tools, 'args': [cmd_obj], 'vld_cmd_args': ['reset']},
               {'cmd': 'cd', 'func': change_dir, 'args': [cmd_obj]},
               {'cmd': 'pm', 'func': access_pm, 'args': [cmd_obj]},
               {'cmd': 'run', 'func': run_program, 'args': [cmd_obj]},
               ]


if __name__ == '__main__':
    main()
