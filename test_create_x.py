import os
import shutil

from TNTFS import return_user_names, File
from login import create_user
from user import User
from ChaOS_DevTools import reset_user_csv

user = User('unit_testing_user', 'password', 'standard')


def clean_unit_testing_dir():
    for file in os.listdir('unit_testing'):
        if file != 'metadata.csv':
            try:
                os.remove(f'unit_testing/{file}')
            except OSError:
                shutil.rmtree(f'unit_testing/{file}')


def test_create_f():
    clean_unit_testing_dir()
    testfile = File('testfile.txt', 'file', 'unit_testing/testfile', 'unit_testing', 'System42', ['System42'])
    testfile.create(['silent'])
    assert testfile.metadata_exists()
    assert testfile.isfile()
    assert testfile.filetype == 'txt'
    assert not testfile.validate_access(user)


def test_create_dir():
    testdir = File('testdir', 'dir', 'unit_testing/testdir', 'unit_testing', 'System42', ['System42'])
    testdir.create(['silent'])
    assert testdir.metadata_exists()
    assert testdir.isdir()
    try:
        print(testdir.filetype)
    except Exception:
        assert True
    else:
        assert False
    assert not testdir.validate_access(user)


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
