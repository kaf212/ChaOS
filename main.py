from file import initialize_user_directories, create_file_object, create_file
from login import login


def main():
    initialize_user_directories()
    global user
    user = login()
    command_prompt()


def command_prompt():
    current_directory = f'A:/Users/{user.name}'
    valid_commands = ['create file']
    while True:
        input_command = input(f'{current_directory}>')
        if input_command not in valid_commands:
            print(f'The command "{input_command}" could not be found. \n')

        if input_command == 'create file':
            create_file(user)
