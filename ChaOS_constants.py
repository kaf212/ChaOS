"""
ChaOS_constants.py
"""

from user import User

CHAOS_VERSION = '1.0.0 Beta'
VALID_ACCOUNT_TYPES = ['standard', 'admin', 'dev']
USER_CSV_ATTRIBUTES = ['name', 'password', 'account type']

UI_2_PATH_TRANSLATIONS = {'A:': 'A',
                          'Users': 'ChaOS_Users'
                          }

PATH_2_UI_TRANSLATIONS = {'A': 'A:',
                          'ChaOS_Users': 'Users'
                          }

SYSTEN_FILE_AND_DIR_NAMES = ['A', 'ChaOS_Users', 'metadata.csv']

LOGGING_FORMAT = '[%(levelname)s] %(message)s'
