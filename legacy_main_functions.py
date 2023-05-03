'''
def create_x_old(cmd):
    """
    The top-level command interpreter for anything starting with "create".
    :param cmd:
    :return None:
    """
    logging.basicConfig(format=ChaOS_constants.LOGGING_FORMAT, level=logging.DEBUG)
    try:
        if cmd.perm_arg == 'sudo':
            print_warning(f'You must enter a valid {cmd.pri_arg}name to proceed. ')
            # check if the user didn't forget the name and "sudo" is misinterpreted as the name.
    except IndexError:
        pass
    if cmd.pri_arg == 'file':
        if validate_filetype(cmd.sec_arg, ['.txt']):  # if the file is a txt:
            if not check_file_existence(cr_dir + cmd.sec_arg):  # if the file doesn't exist yet:
                create_file(cr_dir, cmd.sec_arg, user)
            else:
                print_warning(f'The file "{cmd.sec_arg}" already exists. ')
    elif cmd.pri_arg == 'dir':
        if cmd.get_flag('-perm') == 'all_users':
            dir_type = 'communist'
        else:
            dir_type = 'capitalist'
        create_dir(user=user, dir=cr_dir, name=cmd.sec_arg, cmd=cmd, dir_type=dir_type)
    elif cmd.pri_arg == 'user':
        create_user_ui(user, cmd)
        # the difference between create_user() and create_user_ui() is,
        # that the latter prompts for user info in the console.
    else:
        print_warning(f'"{cmd.pri_arg}" is not a valid statement for command "{cmd.cmd}"\n')
'''

'''
def delete_x(cmd):
    """
    The top-level command interpreter for anything starting with "delete".
    Currently only works for txts.
    :param cmd:
    :return None:
    """
    if cmd.pri_arg == 'file':
        if not os.path.isfile(cr_dir + "/" + cmd.sec_arg):
            print_warning(f'The file "{cr_dir + "/" + cmd.sec_arg}" is not a file or does not exist. ')
            return None
        if validate_file_alteration(cmd.sec_arg, user):  # make sure the user isn't deleting any system files
            file = File()
            file.select(cmd.sec_arg, cr_dir=cr_dir,)
            file.recycle()
    elif cmd.pri_arg == 'user':
        delete_user_safe(user, cmd.sec_arg)
    elif cmd.pri_arg == 'dir':
        target_dir = translate_ui_2_path(cmd.sec_arg)
        if not os.path.isdir(cr_dir + '/' + target_dir):
            print_warning(f'The directory "{cmd.sec_arg}" does not exist. ')
            return None
        if not validate_file_access():
            return None
        # make sure he has access permission
        if not validate_dir_alteration(target_dir, user):  # make sure he's not deleting a system directory
            return None
        if target_dir == 'Recycling bin':
            print_warning('You cannot delete the recycling bin. ')
            return None
        if cr_dir in ['A', 'A/ChaOS_Users']:
            delete_dir(target_dir, cr_dir)
        else:
            recycle(target_dir, cr_dir)
            # delete_dir_ui(cr_dir, target_dir)
    else:
        print_warning(f'"{cmd.pri_arg}" is not a valid statement for command "{cmd.cmd}"\n')
'''

'''
def burn_x(cmd):
    """
    Contrary to deleting, burning removes data from its pathetic existence with no steps inbetween.
    :param cmd:
    :return:
    """
    path = f'{cr_dir}/{cmd.sec_arg}'
    if cmd.pri_arg == 'dir':
        if os.path.isdir(f'{cr_dir}/{cmd.sec_arg}'):
            if validate_file_access(cr_dir, cmd.sec_arg, user, cmd):
                if cmd.sec_arg == 'Recycling bin':
                    if input_y_n(f'Burn recycling bin? > ') == 'y':
                        shutil.rmtree(path)
                        os.mkdir(path)
                        create_md_file(path)
                        syslog('deletion', f'burned recycling bin. ')
                        print_success(f'Burned "{cmd.sec_arg}" successfully. ')
                else:
                    if cmd.sec_arg not in ChaOS_constants.SYSTEM_DIR_NAMES:
                        if input_y_n(f'Burn "{cmd.sec_arg}"? > ') == 'y':
                            shutil.rmtree(path)
                            delete_metadata(cmd.sec_arg, cr_dir)
                            syslog('deletion', f'burned directory "{translate_path_2_ui(path)}". ')
                            print_success(f'Burned "{cmd.sec_arg}" successfully. ')
                    else:
                        print_warning('You cannot burn system directories. ')
    elif cmd.pri_arg == 'file':
        if os.path.isfile(f'{cr_dir}/{cmd.sec_arg}'):
            if cmd.sec_arg not in ChaOS_constants.SYSTEN_FILE_NAMES:
                if input_y_n(f'Burn "{cmd.sec_arg}"? > ') == 'y':
                    os.remove(path)
                    syslog('deletion', f'burned file "{translate_path_2_ui(path)}". ')
                    print_success(f'Burned "{cmd.sec_arg}" successfully. ')
            else:
                print_warning(f'You cannot burn a system file. ')
        else:
            print_warning(f'"{path}" is not a file. ')
'''

'''
def edit_x(cmd):
    """
    The top-level command interpreter dor anything starting with "edit".
    Supports both txts and users.
    :param cmd:
    :return None:
    """

    if cmd.perm_arg == 'sudo':
        print_warning(f'You must enter a valid {cmd.pri_arg}name to proceed. ')
    # check if the user didn't forget the name and "sudo" is misinterpreted as the name.

    else:

        if cmd.pri_arg == 'file':
            if check_file_existence(cr_dir + "/" + cmd.sec_arg):
                if validate_filetype(cmd.sec_arg, ['.txt']):
                    edit_txt(cr_dir + "/" + cmd.sec_arg)
            else:
                print_warning(f'File "{cmd.sec_arg}" does not exist. ')

        elif cmd.pri_arg == 'user':
            if cmd.perm_arg == 'sudo':
                edit_user(cmd)
            elif cmd.sec_arg != user.name and user.account_type not in ['admin', 'dev']:
                print_warning('You need administrator privileges to edit another user. ')
            else:
                edit_user(cmd)
'''