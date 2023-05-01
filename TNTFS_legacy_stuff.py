import csv
import os
import shutil
import datetime

import ChaOS_constants
from colors import print_warning, print_success
from TNTFS import translate_path_2_ui, File, split_path
from system import syslog
from input import input_y_n


def delete_dir(dir_name, directory):
    path = directory + '/' + dir_name
    print(path)
    try:
        shutil.rmtree(path)
        delete_metadata(dir_name, directory)
        syslog('deletion', f'deleted directory "{translate_path_2_ui(path)}"')
    except FileNotFoundError:
        print_warning(f'The directory "{translate_path_2_ui(path)}" does not exist')
    else:
        print_success(f'Deleted "{translate_path_2_ui(path)}". ')


def create_dir(user, dir, name, dir_type, cmd=None):
    name_valid = True
    for char in [' ', '..', '.', '...', '/', "'", '"']:
        if char in name:
            name_valid = False
    if dir_type not in ChaOS_constants.VALID_DIR_TYPES:
        raise ValueError(f'Invalid dir_type "{dir_type}" given. ')
    if not name_valid:
        print_warning(f'"{name}" contains illegal characters. ')
        return None
    access_permission = user.name  # the default access permission is creator only
    if cmd:
        access_permission = cmd.get_flag('-perm')
        if access_permission is None:
            access_permission = user.name
    if not dir.endswith('/'):
        path = dir + '/' + name
    else:
        path = dir + name
    try:
        os.mkdir(path, 0o777)
        # log_file_metadata(user, name, access_permission, dir, dir_type=dir_type)
        syslog('creation', f'created directory "{translate_path_2_ui(path)}"')
    except FileExistsError:
        print_warning(f'The directory "{name}" already exists. ')
    else:
        print_success(f'Directory "{name}" has been created in {translate_path_2_ui(path)}. ')


"""
def validate_dir_access(parent_dir: str, dirname: str, user, cmd) -> bool:

    metadata = read_file_metadata(file=None)
    owner = metadata['owner']
    owner_account_type = metadata['owner_account_type']
    access_permission = metadata['access_permission']

    conditions = [f'{parent_dir}/{dirname}' in ['A/', 'A', 'A/ChaOS_Users'],
                  access_permission == user.name,
                  access_permission == 'all_users',
                  access_permission == user.account_type,
                  user.account_type == 'dev',
                  cmd.perm_arg == 'sudo' and owner_account_type != 'dev'
                  ]

    for cond in conditions:
        if cond:
            return True

    if user.account_type != 'dev' and owner_account_type == 'dev':
        print_warning("You need developer privileges to access another dev's directory. ")
        return False

    if user.account_type not in ['admin', 'dev'] and owner != user.name:
        print_warning("You need administrator privileges to access another user's directory. ")
        return False
"""


def validate_file_alteration(filename, user):
    if filename not in ChaOS_constants.SYSTEN_FILE_NAMES:
        return True

    if user.account_type != 'dev':
        print_warning('You need developer privileges to alter a system file. ')
        return False

    conf = input('You are about to delete a system file, type "iknowwhatimdoing" to proceed. ')
    if conf == 'iknowwhatimdoing':
        return True
    else:
        print_warning('File deletion was aborted. ')
        return False


def validate_dir_alteration(dirname, user):
    if dirname in ChaOS_constants.SYSTEM_DIR_NAMES and user.account_type != 'dev':
        print_warning('You need developer privileges to alter a system directory. ')
        return False
    else:
        return True


def validate_file_access(user, path):
    file = File()
    file.select(location=None, trg_name=path)  # path exists, so cr_dir is obsolete for selection

    conditions = ['all_users' in file.access_perm,
                  user.name in file.access_perm,
                  user.account_type in file.access_perm]

    for condition in conditions:
        if condition:
            return True

    print_warning(f'Access denied to "{file.path}". ')
    return False


def delete_metadata(dirname, parent_dir):
    dirname = dirname.lower()

    md_path = f'{parent_dir}/metadata.csv'
    with open(md_path, 'r') as md_csv:
        attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
        next(md_csv)
        csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
        temp_dict_list = []
        for line in csv_reader:
            if not line['dirname'] == dirname:
                temp_dict_list.append(line)
        md_csv.close()

    with open(md_path, 'w') as md_csv:
        attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
        csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
        csv_writer.writeheader()
        for line in temp_dict_list:
            csv_writer.writerow(line)
        md_csv.close()


def create_md_file(location):
    with open(f'{location}/metadata.csv', 'w') as md:
        csv_writer = csv.DictWriter(md, fieldnames=ChaOS_constants.METADATA_CSV_ATTRIBUTES)
        csv_writer.writeheader()


def read_file_metadata(file: File) -> dict:
    md_path = 'A/System42/metadata/file_metadata.csv'
    if os.path.exists(md_path):
        with open(md_path, 'r') as md_csv:
            attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
            csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
            dir_metadata = None
            for line in csv_reader:
                if line['path'] == file.path:
                    dir_metadata = line
            if not dir_metadata:
                raise Exception(f'No metadata found for "{file.path}"')

            return dir_metadata
    else:
        raise FileNotFoundError(f'metadata.csv not found in {md_path}. ')


"""

 def create_file(dir, name, user):
     name_valid = True
     for char in [' ', '..', '...', '/', "'", '"']:
         if char in name:
             name_valid = False

     if name_valid:
         path = dir + '/' + name
         now = datetime.now()
         now = datetime.strftime(now, '%d.%m.%Y %H:%M')
         if not check_file_existence(path):
             if path.endswith('.txt'):
                 header = f'{name} created on the {now} by {user.name} with ChaOS {ChaOS_constants.CHAOS_VERSION}'
                 header_line = ''
                 for i in range(len(list(header))):
                     header_line += '-'
                 with open(path, 'w', 1) as f:
                     f.write(header_line + '\n')
                     f.write(header + '\n')
                     f.write(header_line + '\n')
                     f.write('\n')
                     f.close()
                 syslog('creation', f'created file "{translate_path_2_ui(path)}"')
                 print_success(f'Created file {name} in {translate_path_2_ui(path)}. ')
         else:
             print_warning(f'{name} already exists in {dir}. ')
     else:
         print_warning(f'{name} contains illegal characters. ')

"""


def find_file(user):
    while True:
        input_filename = input('Filename + type > ')
        directory = os.fsencode(f'A/ChaOS_Users/{user.name}')
        found_file_name = None
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename == input_filename:
                found_file_name = os.fsdecode(file)
            else:
                continue
        if found_file_name:
            return found_file_name
        else:
            input('File not found. ')

"""
def recycle(user: User, target_name: str, location: str):
    if os.path.exists(f'{location}/Recycling bin/{target_name}'):
        try:
            os.remove(f'{location}/Recycling bin/{target_name}')
        except PermissionError:
            shutil.rmtree(f'{location}/Recycling bin/{target_name}')
            delete_metadata(target_name, f'{location}/Recycling bin')
    shutil.move(f'{location}/{target_name}', f'{location}/Recycling bin')
    # log metadata in rec bin.
    metadata = read_file_metadata(target_name, location)
    delete_metadata(target_name, location)
    temp_user_obj = create_user_object(metadata['owner'], None, metadata['owner_account_type'])
    log_file_metadata(user)
    syslog('alteration', f'recycled dir "{translate_path_2_ui(location)}"')
    print_success(f'Directory "{location}/{target_name}" recycled successfully. ')
"""

def restore_file(filename, rec_bin_dir):
    og_path = f'{rec_bin_dir}/{filename}'
    rec_bin_dir = split_path(rec_bin_dir)
    rec_bin_dir.remove('Recycling bin')
    rec_bin_dir.pop(-1)
    destination = ''.join(rec_bin_dir)
    shutil.move(og_path, destination)
    print_success(
        f'File "{translate_path_2_ui(og_path)}" restored successfully to "{translate_path_2_ui(destination)}". ')


def move_file(cr_dir, user, cmd_split):
    """
    destination: fully qualified path of the desired destination (A:/Users/kaf221122/Desktop)

    """
    destination = cmd_split[3]
    source = cmd_split[2]
    trg_dirname = destination
    if '/' in destination:
        trg_dirname = destination.partition('/')[-1]

    if os.path.exists(f'{cr_dir}/{source}'):  # if the defined source is in cr_dir
        source = f'{cr_dir}/{source}'
    elif not os.path.exists(source):  # if the source is not fully qualified barebone
        print_warning(f'The target file or directory "{source}" does not exist')
        return None

    if os.path.exists(f'{cr_dir}/{destination}'):  # if the defined destination is in cr_dir
        destination = f'{cr_dir}/{destination}'
    elif not os.path.exists(destination):  # if the destination is not fully qualified barebone
        print_warning(f'The target directory "{destination}" does not exist')
        return None

    for path in [source, destination]:
        if not validate_file_access(user, path):
            return None

    if os.path.exists(f'{destination}') or os.path.exists('INSERT PATH'):
        if input_y_n(f'"{source}" already exists in "{destination}", do you want to overwrite? ') == 'n':
            print_warning(f'Aborted action. ')
            return None
        else:
            if os.path.isdir(destination):
                shutil.rmtree(destination)
            else:
                os.remove(destination)

    if os.path.isdir(source):
        syslog('alteration', f'moved dir "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}". ')
        print_success(
            f' successfully moved dir "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}".')
    else:
        syslog('alteration', f'moved file "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}". ')
        print_success(
            f'successfully moved file "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}". ')

    shutil.move(source, destination)


def select_file(user, cr_dir, trg_name):
    if os.path.exists(trg_name):
        trg_path = trg_name
    elif os.path.exists(f'{cr_dir}/{trg_name}'):
        trg_path = f'{cr_dir}/{trg_name}'
    else:
        print_warning(f'The file or directory "{trg_name}" does not exist. ')
        return False

    if validate_file_access(user, trg_path):
        return trg_path
    else:
        return False


def validate_filetype(filename, valid_filetypes):
    ft_valid = False
    for filetype in valid_filetypes:
        if filename.endswith(filetype):
            ft_valid = True

    if not ft_valid:
        print_warning(f'"{"." + filename.partition(".")[2]}" is not a valid filetype\n')

    return ft_valid
