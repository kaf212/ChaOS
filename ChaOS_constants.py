"""
ChaOS_constants.py
"""

CHAOS_VERSION = '1.0.0 Beta'
VALID_ACCOUNT_TYPES = ['standard', 'admin', 'dev']
USER_CSV_ATTRIBUTES = ['name', 'password', 'account type']
METADATA_CSV_ATTRIBUTES = ['name', 'type', 'path', 'location', 'owner', 'access_perm']
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
              'mv': 'move',

              'f': 'file',
              'd': 'dir',
              'u': 'user',

              'rec': 'Recycling_bin'

              }

STANDARD_USER_SUBDIRS = ['Documents', 'Desktop', 'Recycling_bin']

SYSTEN_FILE_NAMES = ['metadata.csv']

SYSTEM_DIR_NAMES = ['A', 'ChaOS_Users']

LOGGING_FORMAT = '[%(levelname)s] %(message)s'
