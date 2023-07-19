import shutil
from colors import print_warning, print_blue, print_success
import pip
from ftplib import FTP
import os


AVAILABLE_PACKAGES = {'calc', 'dms3', 'cdbms', 'test'}


def import_functions(module_name: str, function_names: list) -> tuple:
    functions = []
    for func_name in function_names:
        impmodule = __import__(module_name, fromlist=[func_name])
        functions.append(getattr(impmodule, func_name))

    return tuple(functions)


def pm_install(cmd):
    if cmd.sec_arg not in AVAILABLE_PACKAGES:
        print_warning(f'There is no ChaosPack named "{cmd.sec_arg}".')
        return None

    ftp_address = "192.168.1.86"
    ftp_username = "root"
    ftp_password = "1234"
    dir_to_download = f"{cmd.sec_arg}"
    target_dir = f"A/System42/programs/{cmd.sec_arg}"  # Update with the desired directory path
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_address)
        ftp.login(user=ftp_username, passwd=ftp_password)

        # Set the directory (if necessary)
        # ftp.cwd('/path/to/directory')

        # Download the file
        local_file_path = target_dir + '/' + dir_to_download
        try:
            os.mkdir(target_dir)
        except FileExistsError:
            print_warning(f'Package "{cmd.sec_arg}" is already installed on this computer.')
            return None

        with open(local_file_path, 'wb') as file:
            ftp.retrbinary('RETR ' + f'ChaOS_packages/{dir_to_download}', file.write)

        # Close the FTP connection
        ftp.quit()
    except Exception as err:
        print_warning(err)


def pm_uninstall(cmd):
    if cmd.sec_arg not in AVAILABLE_PACKAGES:
        print_warning(f'There is no package named "{cmd.sec_arg}".')
        return None
    try:
        shutil.rmtree(f'A/System42/programs/{cmd.sec_arg}')
    except FileNotFoundError:
        print_warning(f'The system failed to locate resources for package "{cmd.sec_arg}", '
                      f'consider contacting a developer.')

    print_success(f'Successfully uninstalled package "{cmd.sec_arg}".')


def pm_reinstall(cmd):
    if cmd.sec_arg not in AVAILABLE_PACKAGES:
        print_warning(f'There is no package named "{cmd.sec_arg}".')
        return None
    try:
        shutil.rmtree(f'A/System42/programs/{cmd.sec_arg}')
        pm_install(cmd)
    except FileNotFoundError:
        print_warning(f'The system failed to locate resources for package "{cmd.sec_arg}", '
                      f'consider contacting a developer.')


def install_python_package(py_pack, chaos_pack):
    print_blue(f'Installing resources for {chaos_pack}... ')
    pip.main(['install', py_pack])
    print_success(f'Successfully installed resources for {chaos_pack}. ')
