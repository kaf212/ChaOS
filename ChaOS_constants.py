"""
ChaOS_constants.py
"""

CHAOS_VERSION = '1.0.0 Beta'
VALID_ACCOUNT_TYPES = ['standard', 'admin', 'dev']
USER_CSV_ATTRIBUTES = ['name', 'password', 'account type']
SYSLOG_CSV_ATTRIBUTES = ['ID', 'category', 'msg']
SYSLOG_CATEGORIES = ['command', 'creation', 'deletion', 'alteration']
UI_2_PATH_TRANSLATIONS = {'A:': 'A',
                          'Users': 'ChaOS_Users'
                          }

PATH_2_UI_TRANSLATIONS = {'A': 'A:',
                          'ChaOS_Users': 'Users'
                          }

SYSTEN_FILE_NAMES = ['metadata.csv']

SYSTEM_DIR_NAMES = ['A', 'ChaOS_Users']

LOGGING_FORMAT = '[%(levelname)s] %(message)s'
