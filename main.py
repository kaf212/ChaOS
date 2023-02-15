from file import initialize_user_directories, create_file, find_file, read_txt
from login import login


def main():
    initialize_user_directories()
    global user
    user = login()
    command_prompt()


def command_prompt():
    current_directory = f'A:/Users/{user.name}'
    while True:
        input_command = input(f'{current_directory}>')

        if input_command == 'create file':
            create_file(owner=user)

        if input_command == 'read file':
            filename = find_file(user)
            read_txt(filename, user)
        else:
            print(f'The command "{input_command}" could not be found. \n')