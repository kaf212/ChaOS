from file import initialize_user_directories, create_file, find_file, read_txt, validate_filetype, check_file_existence, \
    delete_file, edit_txt
from input import input_y_n
from login import login


def main():
    initialize_user_directories()
    global user
    user = login()
    command_prompt()


def command_prompt():
    global cr_dir
    cr_dir = f'ChaOS_Users/{user.name}'
    cr_dir_ui = f'A:/Users/{user.name}'
    while True:
        input_command = input(f'{cr_dir_ui}>').lower()

        interpret_command(input_command)


def interpret_command(cmd):
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
        except TypeError:
            print('You must enter a valid command to proceed, type "help" for help. ')

        else:
            print(f'The command "{cmd_split[0]}" does not exist. \n')

    else:
        print('You must enter a valid command to proceed, type "help" for help. ')


def create_x(cmd_split):
    if cmd_split[1] == 'file':
        if validate_filetype(cmd_split[2], ['.txt']):
            if not check_file_existence(cr_dir + cmd_split[2]):
                create_file(cr_dir, cmd_split[2])
            else:
                print(f'The file "{cmd_split[2]}" already exists. ')

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
