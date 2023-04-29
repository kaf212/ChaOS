import os
import shutil

from file import *
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


def test_delete_dir():
    if not os.path.exists('unit_testing/testdir'):
        create_dir(user, 'unit_testing', 'testdir', 'capitalist')
    delete_dir('testdir', 'unit_testing')
    if not os.path.isdir('unit_testing/testdir'):
        try:
            read_file_metadata('testdir', 'unit_testing')
        except Exception:
            assert True
        else:
            print('Directory Metadata was not deleted. ')
            assert False
    else:
        print('Directory was not deleted. ')
        assert False
    clean_unit_testing_dir()


def test_delete_metadata():
    if not check_metadata_existence(user, 'md_testdir', user.name, 'unit_testing', 'capitalist'):
        log_file_metadata(user, 'md_testdir', user.name, 'unit_testing', 'capitalist')

    delete_metadata('md_testdir', 'unit_testing')

    if not check_metadata_existence(user, 'md_testdir', user.name, 'unit_testing', 'capitalist'):
        assert True
