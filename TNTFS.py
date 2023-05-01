import shutil
import csv
from csv_handling import return_user_names, return_users
import os
import ChaOS_constants
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
    location: str = None  # path of the parent dir (A/ChaOS_Users/kaf221122/Desktop)
    owner: str = None
    access_perm: list = field(default_factory=list)

    @property
    def path_ui(self):
        return translate_path_2_ui(self.path)

    @property
    def location_ui(self):
        return translate_path_2_ui(self.location)

    @property
    def filetype(self):
        if self.isfile():
            return self.name.partition(".")[2]
        else:
            raise Exception('Tried accessing filetype of directory object. ')

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

    def init(self, cmd, user: User, cr_dir: str):
        """
        Initializes the empty object with data from the cmd.
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

    def create_phys(self):
        """
        Physically creates the file without any prior validation, be careful using it!
        """
        if self.isfile():  # if the object is a file:
            f = open(self.path, 'w')
            f.close()
        else:
            os.makedirs(self.path)

        if self.isfile():
            syslog('creation', f'Created file "{self.path}"')
        else:
            syslog('creation', f'Created dir "{self.path}"')

    def validate(self, mode=None, valid_filetypes=None):
        def print_warning_silent(output):
            if mode != 'silent':
                print_warning(output)

        if os.path.exists(self.path):
            print_warning_silent(f'The file or directory "{self.name}" already exists. ')
            return False

        illegal_chars = ['..', '/', ' ', "'", '"']
        for char in illegal_chars:
            if char in self.name:
                print_warning_silent(f'The file- or directory name cannot contain "{char}". ')
                return False

        if '.' in self.name and self.type == 'dir':
            print_warning_silent(f'A directory name cannot contain a decimal point. ')
            return False

        if self.name.count('.') > 1:
            print_warning_silent(f'The filename cannot contain > 1 decimal points. ')
            return False

        if self.type not in ['file', 'dir']:
            print_warning_silent(f'"{self.type}" is not a valid type (try "file" or "dir"). ')
            return False

        if self.name in ChaOS_constants.SYSTEM_DIR_NAMES or self.name in ChaOS_constants.SYSTEN_FILE_NAMES:
            print_warning_silent(f"The file- or directory name cannot be a standard system name. ")
            return False

        if self.access_perm:
            for perm in self.access_perm:
                if perm not in return_user_names() and perm not in ChaOS_constants.VALID_ACCOUNT_TYPES:
                    print_warning_silent(f'The user or account type "{perm}" does not exist. ')
                    return False

        if valid_filetypes:  # if valid filetypes have been specified
            ft_valid = False
            for filetype in valid_filetypes:
                if self.name.endswith(filetype):
                    ft_valid = True
            if not ft_valid:
                print_warning_silent(f'"{"." + self.name.partition(".")[2]}" is not a valid filetype\n')
                return False

        return True

    def reset(self):
        for attr, value in self.__dict__.items():
            if type(value) == str and not value.startswith('__'):
                self.__dict__[attr] = None
            elif type(value) == list:
                self.__dict__[attr] = list()

    def select(self, trg_name, location=None):
        """
        Gets the fully qualified path of the target and loads the metadata.
        """
        self.reset()
        trg_name = translate_ui_2_path(trg_name)
        if os.path.exists(trg_name):
            self.path = trg_name
            self.load_metadata()
            return True
        if os.path.exists(f'{location}/{trg_name}'):
            self.path = f'{location}/{trg_name}'
            self.load_metadata()
            return True
        print_warning(f'The file or directory "{trg_name}" does not exist in "{location}". ')
        return False

    def validate_access(self, user):   # TODO: looks incomplete
        pos_conditions = ['all_users' in self.access_perm,
                          user.name in self.access_perm,
                          user.account_type in self.access_perm]

        for condition in pos_conditions:
            if condition:
                return True

        print_warning(f'Access denied to "{self.path}". ')
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
            if perm != 'all_users' and perm not in return_user_names() \
                    and perm not in ChaOS_constants.VALID_ACCOUNT_TYPES:
                raise ValueError(f'Invalid access permission "{perm}" given. ')

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
            # next(md_csv)
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
        """
        Completely wipes the file out of existence.
        """
        self.delete_metadata()
        if self.isdir():
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)

    def empty(self):
        """
        Removes all contents from a directory.
        """
        if self.isfile():
            raise Exception('Tried emtying a file. ')
        for filename in os.listdir(self.path):
            file = File()
            file.select(trg_name=filename, location=self.path)
            file.delete()
            del file   # To definitely avoid interference amongst all the file objects in the loop.

    def recycle(self):
        if os.path.exists(f'{self.location}/Recycling_bin/{self.name}'):
            try:
                os.remove(f'{self.location}/Recycling_bin/{self.name}')
            except PermissionError:
                shutil.rmtree(f'{self.location}/Recycling_bin/{self.name}')

            self.delete_metadata()

            default_rec_bin_path = f'{self.location}/Recycling_bin'
            if os.path.exists(default_rec_bin_path):
                self.move(default_rec_bin_path)
            else:  # if the file is located in a directory without recycling bin, it is moved to the owners rec bin.
                self.move(f'A/ChaOS_Users/{self.owner}/Recycling_bin')

            if self.isdir():
                syslog('alteration', f'recycled dir "{translate_path_2_ui(self.location)}"')
                print_success(f'Directory "{self.path}" recycled successfully. ')
            else:
                syslog('alteration', f'recycled file "{translate_path_2_ui(self.location)}"')
                print_success(f'File "{self.path}" recycled successfully. ')

    def restore(self, cr_dir):
        rec_bin_dir = f'{cr_dir}/Recycling_bin'
        if not os.path.exists(rec_bin_dir):
            print_warning(f'There is no recycling bin in "{translate_path_2_ui(cr_dir)}". ')
            return None

        self.move(cr_dir)

    def move(self, new_location):
        if not os.path.exists(new_location):
            raise NotADirectoryError(f'provided new location "{new_location}" does not exsit.')

        new_path = f'{new_location}/{self.name}'
        if os.path.exists(new_path):
            redundant_file = File()
            redundant_file.select(trg_name=new_path)
            redundant_file.delete()

        shutil.move(self.path, new_path)
        self.path = new_location
        self.delete_metadata()  # delete the old metadata
        self.log_metadata()  # log the new, correct metadata

    def edit_ui(self):
        if self.filetype not in ['txt']:
            print_warning(f'You cannot edit this filetype. ')
            return None

        user_text = input('Text > ')
        with open(self.path, 'a+') as f:
            f.write('\n')
            f.write(user_text)
        syslog('alteration', f'edited file "{translate_path_2_ui(self.path)}"')


def read_txt(directory, name):
    path = directory + '/' + name
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
                                  location=f'A/ChaOS_Users/{temp_user_obj.name}', owner=temp_user_obj.name,
                                  access_perm=[temp_user_obj.name])
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
                dir_obj.select(location='A/ChaOS_Users', trg_name=d)
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
            usr_dir = File(username, 'dir', f'A/ChaOS_Users/{username}', 'A/ChaOS_Users', username, [username])
            usr_dir.log_metadata()


def edit_txt(path):
    user_text = input('Write > ')
    with open(path, 'a+') as f:
        f.write('\n')
        f.write(user_text)
        f.close()
    syslog('alteration', f'edited file "{translate_path_2_ui(path)}"')


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
