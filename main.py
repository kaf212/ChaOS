from file import initialize_user_directories, create_file, find_file, read_txt
from login import login, create_user


def main():
    initialize_user_directories()
    global user
    user = login()
    command_prompt()


def command_prompt():
    current_directory = f'A:/Users/{user.name}'
    while True:
        input_command = input(f'{current_directory}>').lower()

        interpret_command(input_command)


def interpret_command(cmd):
    cmd_split = cmd.split()
    if cmd_split[0] == 'create':
        create_x(cmd_split)

    elif cmd_split[0] == 'read':
        read_x(cmd_split)

    else:
        print(f'The command "{cmd_split[0]}" does not exist. \n')


def create_x(cmd_split):
    if cmd_split[1] == 'file':
        create_file(user)
    elif cmd_split[1] == 'user':
        pass
    else:
        print(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}"\n')


def read_x(cmd_split):
    if cmd_split[1] == 'file':
        pass
    else:
        print(f'"{cmd_split[1]}" is not a valid statement for command "{cmd_split[0]}\n')
