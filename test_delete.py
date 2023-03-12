import os
import shutil

from file import *
from login import create_user
from user import User
from ChaOS_DevTools import reset_user_csv

user = User('unit_testing_user', 'password', 'standard')


def clean_unit_testing_dir():
    for file in os.listdir('A/unit_testing'):
        if file != 'metadata.csv':
            try:
                os.remove(f'A/unit_testing/{file}')
            except OSError:
                shutil.rmtree(f'A/unit_testing/{file}')


def test_delete_dir():
    if not os.path.exists('A/unit_testing/testdir'):
        create_dir(user, 'A/unit_testing', 'testdir', 'capitalist')
    delete_dir('testdir', 'A/unit_testing')
    if not os.path.isdir('A/unit_testing/testdir'):
        try:
            read_dir_metadata('testdir', 'A/unit_testing')
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
    if not check_metadata_existence(user, 'md_testdir', user.name, 'A/unit_testing', 'capitalist'):
        log_dir_metadata(user, 'md_testdir', user.name, 'A/unit_testing', 'capitalist')

    delete_metadata('md_testdir', 'A/unit_testing')

    if not check_metadata_existence(user, 'md_testdir', user.name, 'A/unit_testing', 'capitalist'):
        assert True
