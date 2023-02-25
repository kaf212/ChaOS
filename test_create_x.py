import os
import shutil

from file import create_file, create_dir, return_user_names
from login import create_user
from user import User
from ChaOS_DevTools import reset_user_csv

user = User('unit_testing_user', 'password', 'standard')


def clean_unit_testing_dir():
    for file in os.listdir('A/unit_testing'):
        try:
            os.remove(f'A/unit_testing/{file}')
        except OSError:
            shutil.rmtree(f'A/unit_testing/{file}')


def test_create_file():
    try:
        create_file('A/unit_testing', 'test_create_file.txt', user)
    except FileExistsError:
        os.remove('A/unit_testing/test_create_file.txt')
        create_file('A/unit_testing', 'test_create_file.txt', user)
    filenames = []
    for file in os.listdir('A/unit_testing'):
        filenames.append(file)

    assert 'test_create_file.txt' in filenames

    clean_unit_testing_dir()


def test_create_directory():

    if not os.path.exists('A/unit_testing'):
        os.mkdir('A/unit_testing')

    try:
        create_dir(user, 'A/unit_testing', 'test_create_dir')
    except FileExistsError:
        os.remove('A/unit_testing/test_create_dir')
        create_dir(user, 'A/unit_testing', 'test_create_dir')
    dirnames = []
    for file in os.listdir('A/unit_testing'):
        dirnames.append(file)

    assert 'test_create_dir' in dirnames

    clean_unit_testing_dir()


def test_create_user():
    create_user(user.name, user.password, user.account_type)
    user_present_in_csv = False
    if user.name in return_user_names():
        user_present_in_csv = True

    user_dirs = []
    for user_dir in os.listdir('A/ChaOS_Users'):
        user_dirs.append(user_dir)

    user_dir_created = False
    if user.name in user_dirs:
        user_dir_created = True

    assert user_present_in_csv and user_dir_created
    shutil.rmtree(f'A/ChaOS_Users/{user.name}')  # delete the test directory
    reset_user_csv('-hard')





