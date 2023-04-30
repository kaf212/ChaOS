import shutil
import csv
from csv_handling import return_user_names, return_users
import os
from datetime import datetime
import ChaOS_constants
from input import input_y_n
from user import create_user_object, User
import logging
from system import syslog
from colors import *
from dataclasses import dataclass, field


@dataclass
class File:
    name: str = None
    type: str = None
    path: str = None  # fully qualified path to the file (A/ChaOS_Users/kaf221122/Desktop/file.txt)
    location: str = None   # path of the parent dir (A/ChaOS_Users/kaf221122/Desktop)
    owner: str = None
    access_perm: list = field(default_factory=list)

    @property
    def path_ui(self):
        return translate_path_2_ui(self.path)

    @property
    def location_ui(self):
        return translate_path_2_ui(self.location)

    def isdir(self):
        if self.type == 'dir':
            return True
        return False

    def isfile(self):
        if self.type == 'file':
            return True
        return False

    def is_communist(self):
        if 'all_users' in self.access_perm:
            return True
        return False

    def is_capitalist(self):
        """
        Checks if any other people other than the owner are permitted to access the file.
        """
        for perm in self.access_perm:
            if perm != self.owner:  # if the permitted person is not the owner himself
                return False
        return True

    def create(self, cmd, user: User, cr_dir: str):
        """
        Initializes the empty object with data from the cmd, validates it and if validated, physically creates the file in
        the desired location.
        """
        self.reset()
        self.name = cmd.sec_arg
        self.type = cmd.pri_arg
        self.path = f'{cr_dir}/{self.name}'
        self.location = cr_dir
        self.owner = user.name
        if cmd.flag_exists:
            self.access_perm = cmd.get_flag('-p')

        if not self.validate():
            self.reset()
            return False

        self.create_phys()

    def create_phys(self):
        """
        Physically creates the file without any prior validation, be careful using it!
        """
        if self.isfile():  # if the object is a file:
            f = open(self.path, 'w')
            f.close()
        else:
            os.makedirs(self.path)

    def validate(self, mode=None):
        if os.path.exists(self.path):
            if mode != 'silent':
                print_warning(f'The file or directory "{self.name}" already exists. ')
            return False

        illegal_chars = ['..', '/', ' ', "'", '"']
        for char in illegal_chars:
            if char in self.name:
                if mode != 'silent':
                    print_warning(f'The file- or directory name cannot contain "{char}". ')
                return False

        if '.' in self.name and self.type == 'dir':
            if mode != 'silent':
                print_warning(f'A directory name cannot contain a decimal point. ')
            return False

        if self.type not in ['file', 'dir']:
            if mode != 'silent':
                print_warning(f'"{self.type}" is not a valid type (try "file" or "dir"). ')
            return False

        if self.name in ChaOS_constants.SYSTEM_DIR_NAMES or self.name in ChaOS_constants.SYSTEN_FILE_NAMES:
            if mode != 'silent':
                print_warning(f"The file- or directory name cannot be a standard system name. ")
            return False

        if self.access_perm:
            for perm in self.access_perm:
                if perm not in return_user_names() and perm not in ChaOS_constants.VALID_ACCOUNT_TYPES:
                    if mode != 'silent':
                        print_warning(f'The user or account type "{perm}" does not exist. ')
                    return False

        return True

    def reset(self):
        for attr, value in self.__dict__.items():
            if type(value) == str and not value.startswith('__'):
                self.__dict__[attr] = None
            elif type(value) == list:
                self.__dict__[attr] = list()

    def select(self, cr_dir, trg_name):
        """
        Gets the fully qualified path of the target and loads the metadata.
        """
        self.reset()
        trg_name = translate_ui_2_path(trg_name)
        if os.path.exists(trg_name):
            self.path = trg_name
            self.load_metadata()
            return True
        if os.path.exists(f'{cr_dir}/{trg_name}'):
            self.path = f'{cr_dir}/{trg_name}'
            self.load_metadata()
            return True
        print_warning(f'The file or directory "{trg_name}" does not exist in "{cr_dir}". ')
        return False

    def load_metadata(self):
        if not os.path.exists('A/System42/metadata/file_metadata.csv'):
            raise FileNotFoundError('System metadata directory could not be found. ')

        with open('A/System42/metadata/file_metadata.csv', 'r') as f:
            reader = csv.DictReader(f, fieldnames=ChaOS_constants.METADATA_CSV_ATTRIBUTES)
            metadata = None
            for line in reader:
                if line['path'] == self.path:
                    metadata = line
            if metadata is None:
                raise Exception(f'Metadata for "{self.path}" could not be found. ')

        self.name = metadata['name']
        self.type = metadata['type']
        self.path = metadata['path']
        self.location = metadata['location']
        self.owner = metadata['owner']
        self.access_perm = metadata['access_perm']

    def log_metadata(self):
        for perm in self.access_perm:
            if perm not in [return_user_names(), 'all_users', ChaOS_constants.VALID_ACCOUNT_TYPES]:
                raise ValueError(f'Invalid access permission "{self.access_perm}" given. ')

        if not os.path.isdir(self.location):
            raise NotADirectoryError(f'{self.location} is not a directory. ')

        md_path = f'A/System42/metadata/file_metadata.csv'
        if not os.path.exists(md_path):
            with open(md_path, 'w') as md_csv:
                attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
                csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
                csv_writer.writeheader()

        if not self.check_metadata_existence():
            with open(md_path, 'a+') as md_csv:
                attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
                csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
                csv_writer.writerow(
                    {'name': self.name.lower(), 'type': self.type, 'path': self.path,
                     'location': self.location, 'access_perm': self.access_perm})

    def check_metadata_existence(self):
        md_path = f'A/System42/metadata/file_metadata.csv'
        with open(md_path, 'r') as md_csv:
            attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
            next(md_csv)
            csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
            for line in csv_reader:
                if line['path'] == self.path:
                    return True
            return False

    def delete_metadata(self):
        md_path = 'A/System42/metadata/file_metadata.csv'
        with open(md_path, 'r') as md_csv:
            attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
            next(md_csv)
            csv_reader = csv.DictReader(md_csv, fieldnames=attributes)
            temp_dict_list = []
            for line in csv_reader:
                if not line['path'] == self.path:
                    temp_dict_list.append(line)

        with open(md_path, 'w') as md_csv:
            attributes = ChaOS_constants.METADATA_CSV_ATTRIBUTES
            csv_writer = csv.DictWriter(md_csv, fieldnames=attributes)
            csv_writer.writeheader()
            for line in temp_dict_list:
                csv_writer.writerow(line)

    def delete(self):
        self.delete_metadata()
        if self.isdir():
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)
        self.reset()

    def recycle(self):
        pass


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



def read_txt(dir, name):
    path = dir + '/' + name
    with open(path, 'r') as f:
        print(f'-- {name} --\n')
        print(f.read())
        print(f'\n-- {name} --\n')
        f.close()


def initialize_A_drive():
    logging_format = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)
    try:
        os.makedirs('A/ChaOS_Users', 0o777)
    except FileExistsError:
        pass
    try:
        os.makedirs('A/System42/metadata')
    except FileExistsError:
        pass

    try:
        f = open('A/System42/metadata/file_metadata.csv', 'w')
        f.close()
    except FileExistsError:
        pass

    dir_obj = File('ChaOS_Users', 'dir', 'A/ChaOS_Users', 'A', 'System42', ['all_users'])
    dir_obj.log_metadata()
    usernames = return_user_names()
    all_users = return_users()

    for username in usernames:
        path = 'A/ChaOS_Users/' + username
        temp_user_obj = None
        for line in all_users:
            if line['name'] == username:
                temp_user_obj = create_user_object(username=line['name'], password='None',  # create a temporary user
                                                   account_type=line['account type'])
        if not os.path.exists(path):  # create the primary user dir if not exists already
            os.mkdir(path)

        for subdir in ChaOS_constants.STANDARD_USER_SUBDIRS:
            usr_subdir_obj = File(name=subdir, type='dir', path=f'A/ChaOS_Users/{temp_user_obj.name}/{subdir}',
                                  location=f'A/ChaOS_Users/{temp_user_obj.name}', owner=temp_user_obj.name, access_perm=[temp_user_obj.name])
            usr_subdir_obj.log_metadata()
            if usr_subdir_obj.validate(mode='silent'):
                usr_subdir_obj.create_phys()

    for username in usernames:
        initialize_user_dir_metadata(username)


def reset_user_dirs(reset_flag=None):
    """
    Contrary to initialize_user_dirs(), this function deletes everything except standard direcotries of
    existing users.
    :return:
    """
    if reset_flag is None:
        initialize_A_drive()
        for d in os.listdir('A/ChaOS_Users'):
            if os.path.isdir(f'A/ChaOS_Users/{d}') and f'A/ChaOS_Users/{d}' not in ChaOS_constants.SYSTEM_DIR_NAMES:
                dir_obj = File()
                dir_obj.select('A/ChaOS_Users', d)
                if dir_obj.owner not in return_user_names() and not dir_obj.is_communist():
                    dir_obj.delete()

    if reset_flag == '-hard':
        for d in os.listdir('A/ChaOS_Users'):
            path = f'A/ChaOS_Users/{d}'
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        initialize_A_drive()


def initialize_user_dir_metadata(username):
    logging_format = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)

    all_users = return_users()

    for line in all_users:
        if line['name'] == username:
            temp_user_obj = create_user_object(username=line['name'], password='None',
                                               account_type=line['account type'])
            log_file_metadata(user=temp_user_obj, file=File(username, 'dir', f'A/ChaOS_Users/{username}', 'A/ChaOS_Users', username, [username]))


def create_md_file(location):
    with open(f'{location}/metadata.csv', 'w') as md:
        csv_writer = csv.DictWriter(md, fieldnames=ChaOS_constants.METADATA_CSV_ATTRIBUTES)
        csv_writer.writeheader()


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


def validate_filetype(filename, valid_filetypes):
    ft_valid = False
    for filetype in valid_filetypes:
        if filename.endswith(filetype):
            ft_valid = True

    if not ft_valid:
        print_warning(f'"{"." + filename.partition(".")[2]}" is not a valid filetype\n')

    return ft_valid


def check_file_existence(path):
    f_exists = os.path.isfile(path)
    return f_exists


def delete_file_ui(path):
    confirmation = input_y_n(f'Delete "{path}" ? > ')
    if confirmation == 'y':
        if check_file_existence(path):
            os.remove(path)
            syslog('deletion', f'deleted file "{path}"')
            print_success(f'Deleted "{path}". ')
        else:
            print_warning("File not found. ")


def delete_dir_ui(directory, dir_name):
    path = directory + '/' + dir_name

    confirmation = input_y_n(f'Delete "{translate_path_2_ui(path)}" ? >')
    if confirmation == 'y':
        delete_dir(path, dir_name, directory)


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


def edit_txt(path):
    user_text = input('Write > ')
    with open(path, 'a+') as f:
        f.write('\n')
        f.write(user_text)
        f.close()
    syslog('alteration', f'edited file "{translate_path_2_ui(path)}"')


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
        log_file_metadata(user, name, access_permission, dir, dir_type=dir_type)
        syslog('creation', f'created directory "{translate_path_2_ui(path)}"')
    except FileExistsError:
        print_warning(f'The directory "{name}" already exists. ')
    else:
        print_success(f'Directory "{name}" has been created in {translate_path_2_ui(path)}. ')


#def validate_dir_access(parent_dir: str, dirname: str, user, cmd) -> bool:
#
#    metadata = read_file_metadata(file=None)
#    owner = metadata['owner']
#    owner_account_type = metadata['owner_account_type']
#    access_permission = metadata['access_permission']
#
#    conditions = [f'{parent_dir}/{dirname}' in ['A/', 'A', 'A/ChaOS_Users'],
#                  access_permission == user.name,
#                  access_permission == 'all_users',
#                  access_permission == user.account_type,
#                  user.account_type == 'dev',
#                  cmd.perm_arg == 'sudo' and owner_account_type != 'dev'
#                  ]
#
#    for cond in conditions:
#        if cond:
#            return True
#
#    if user.account_type != 'dev' and owner_account_type == 'dev':
#        print_warning("You need developer privileges to access another dev's directory. ")
#        return False
#
#    if user.account_type not in ['admin', 'dev'] and owner != user.name:
#        print_warning("You need administrator privileges to access another user's directory. ")
#        return False


def validate_file_access(user, path):
    file = File()
    file.select(cr_dir=None, trg_name=path)  # path exists, so cr_dir is obsolete for selection

    conditions = ['all_users' in file.access_perm,
                  user.name in file.access_perm,
                  user.account_type in file.access_perm]

    for condition in conditions:
        if condition:
            return True

    print_warning(f'Access denied to "{file.path}". ')
    return False




def validate_file_alteration(filename, user):
    logging.basicConfig(level=logging.DEBUG, format=ChaOS_constants.LOGGING_FORMAT)
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


def split_path(path) -> list:
    path_split_total = []
    while True:
        path_split = path.partition('/')
        path_split_total.append(path_split[0])
        path_split_total.append(path_split[1])
        path = path_split[2]
        if '/' not in path_split[2]:
            path_split_total.append(path_split[2])
            break

    return path_split_total


def translate_ui_2_path(ui_path):
    """
    The user sees and enters directories as "A:/Users", but the actual directory would be "A/CHaOS_Users",
    because you obviously can't just create a folder named like a drive.
    This function translates user inputs to an actual path, so it can be processed.
    :param ui_path:
    :return path:
    """
    equivalents = ChaOS_constants.UI_2_PATH_TRANSLATIONS

    ui_path_split = split_path(ui_path)

    path_list = []

    for path in ui_path_split:
        if path in equivalents.keys():
            path = equivalents[path]
        path_list.append(path)

    path = ''.join(path_list)

    return path


def translate_path_2_ui(path):
    """
    The user sees and enters directories as "A:/Users", but the actual directory would be "A/CHaOS_Users",
    because you obviously can't just create a folder named like a drive.
    This function translates an actual path to a simulated one.
    :param path:
    :return ui_path:
    """
    equivalents = ChaOS_constants.PATH_2_UI_TRANSLATIONS

    cr_path_split = split_path(path)

    ui_path_list = []

    for path in cr_path_split:
        if path in equivalents.keys():  # if there's a translation present:
            path = equivalents[path]  # translate it
        ui_path_list.append(path)  # either way, add it to the translated list

    ui_path = ''.join(ui_path_list)  # reconvert the list to a string

    return ui_path


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


def restore_file(filename, rec_bin_dir):
    og_path = f'{rec_bin_dir}/{filename}'
    rec_bin_dir = split_path(rec_bin_dir)
    rec_bin_dir.remove('Recycling bin')
    rec_bin_dir.pop(-1)
    destination = ''.join(rec_bin_dir)
    shutil.move(og_path, destination)
    print_success(
        f'File "{translate_path_2_ui(og_path)}" restored successfully to "{translate_path_2_ui(destination)}". ')


# move f hello.txt a:/Users/seve

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
        print_success(f' successfully moved dir "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}".')
    else:
        syslog('alteration', f'moved file "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}". ')
        print_success(f'successfully moved file "{translate_path_2_ui(source)}" to "{translate_path_2_ui(destination)}". ')

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




