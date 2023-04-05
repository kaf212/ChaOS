CREATE_DEF = 'Is used to create files, directories and other users. Can be used with the keyword "cr".'

READ_DEF = 'Is used for read-only display of txts. ' \
           '\nAlso shows meta information like creator, time of creation and ChaOS version. ' \
           '\nCan be used with the keyword "rd".'

DELETE_DEF = 'Is used for moving files and directories into the recycling bin ' \
             '\n(given the source location was in a non-system directory like A: or A:/Users). ' \
             '\nUsers can be deleted too, but will face immediate termination, not temporary storage in the recycling ' \
             'bin. ' \
             '\nCan be used with the keyword "del".'

BURN_DEF = 'Is used to delete a file or directory without temporary storage in the recycling bin. ' \
           '\nNote that burning the recycling bin will permanently delete every file or directory inside,' \
           '\nbut won’t remove the recycling bin directory itself.'

RESTORE_DEF = 'Is used for restoring files or directories from the recycling bin in the current directory. ' \
              '\nOnly works in non-system directories. Can be used with the keyword "res".'

EDIT_DEF = 'Is used to write to a file (currently only txts) or to change ' \
           '\nuser details like name, password, or account type. ' \
           '\nCan be used with the keywords "alt" or "ed".'

DIR_DEF = 'Is used to display all files or and directories in the current directory.' \
          '\nCan be used with the keyword "d".'

ECHO_DEF = 'Is used to echo a string, there’s no apparent reason for this command’s existence.'

CLEAR_DEF = 'Is used to clear the console of any past in- and outputs. Can be used with the keyword "cl"'

HELP_DEF = 'Is used to get short summarisation and syntax for a command if you’re too lazy to read the documentation.'

DEF_SYSLOG = 'Is used to display all performed actions (executed commands, creations, deletions, alterations etc.)' \
             '\nin the current session. Resets after shutdown.'

DEF_IPCONFIG = 'Is used to display information about the current network and client. '

cmd_def_map = {'create': CREATE_DEF,
               'read': READ_DEF,
               'delete': DELETE_DEF,
               'burn': BURN_DEF,
               'restore': RESTORE_DEF,
               'edit': EDIT_DEF,
               'echo': ECHO_DEF,
               'clear': CLEAR_DEF,
               'syslog': DEF_SYSLOG,
               'ipconfig': DEF_IPCONFIG
               }

cmd_usage = {'create': 'cr <object> <name>',
             'read': 'rd <object> <name>',
             'delete': 'del <object> <name>',
             'burn': 'burn <object> <name>',
             'restore': 'res <object> <name>',
             'edit': 'alt  <object> <name>',
             'cd': 'cd <target dir>',
             'dir': 'd',
             'clear': 'cl',
             'echo': 'echo <string>',
             'help': 'help <target cmd> (-def)',
             'shutdown': 'sd (t- <seconds>)',
             'syslog': 'syslog',
             'ipconfig': 'ipconfig (/all)'
             }
