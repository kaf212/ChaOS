import os
import shutil

from TNTFS import *
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


def test_delete_file():
    clean_unit_testing_dir()
    testfile = File('testfile.txt', 'file', 'unit_testing/testfile', 'unit_testing', 'System42', ['System42'])
    testfile.create(['silent'])
    testfile.delete()
    assert not testfile.metadata_exists()


def test_delete_metadata():
    clean_unit_testing_dir()
    testfile = File('testfile.txt', 'file', 'unit_testing/testfile', 'unit_testing', 'System42', ['System42'])
    testfile.create(['silent'])
    testfile.delete_metadata()
    assert not testfile.metadata_exists()
