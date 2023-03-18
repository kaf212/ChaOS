"""
ChaOS_constants.py
"""

CHAOS_VERSION = '1.0.0 Beta'
VALID_ACCOUNT_TYPES = ['standard', 'admin', 'dev']
USER_CSV_ATTRIBUTES = ['name', 'password', 'account type']
METADATA_CSV_ATTRIBUTES = ['dirname', 'owner', 'owner_account_type', 'access_permission', 'dir_type']
VALID_DIR_TYPES = ['personal', 'capitalist', 'communist']
SYSLOG_CSV_ATTRIBUTES = ['ID', 'time', 'category', 'msg']
SYSLOG_CATEGORIES = ['command', 'creation', 'deletion', 'alteration']
UI_2_PATH_TRANSLATIONS = {'A:': 'A',
                          'Users': 'ChaOS_Users'
                          }

PATH_2_UI_TRANSLATIONS = {'A': 'A:',
                          'ChaOS_Users': 'Users'
                          }

CMD_SHORTS = {'cr': 'create',
              'rd': 'read',
              'del': 'delete',
              'ed': 'edit',
              'alt': 'edit',
              'cl': 'clear',
              'sd': 'shutdown',
              'sl': 'syslog',
              'res': 'restore',

              'f': 'file',
              'd': 'dir',
              'u': 'user',

              'rec': 'Recycling bin'

              }

STANDARD_USER_SUBDIRS = ['Documents', 'Desktop', 'Recycling bin']

SYSTEN_FILE_NAMES = ['metadata.csv']

SYSTEM_DIR_NAMES = ['A', 'ChaOS_Users']

LOGGING_FORMAT = '[%(levelname)s] %(message)s'
