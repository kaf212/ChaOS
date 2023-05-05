import shutil
from colors import print_warning, print_blue, print_success
import pip
from dataclasses import dataclass, field

AVAILABLE_PACKAGES = {'calc'}


def pm_install(cmd):
    if cmd.sec_arg not in AVAILABLE_PACKAGES:
        print_warning(f'There is no ChaosPack named "{cmd.sec_arg}".')
        return None
    try:
        shutil.copytree(f'ChaOS_packages/{cmd.sec_arg}', f'A/System42/programs/{cmd.sec_arg}')
    except FileNotFoundError:
        print_warning(f'The system failed to locate resources for package "{cmd.sec_arg}", '
                      f'consider contacting a developer.')


def pm_uninstall(cmd):
    if cmd.sec_arg not in AVAILABLE_PACKAGES:
        print_warning(f'There is no package named "{cmd.sec_arg}".')
        return None
    try:
        shutil.rmtree(f'A/System42/programs/{cmd.sec_arg}')
    except FileNotFoundError:
        print_warning(f'The system failed to locate resources for package "{cmd.sec_arg}", '
                      f'consider contacting a developer.')
        

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
    pip.main(['-m install', py_pack])
    print_success(f'Successfully installed resources for {chaos_pack}. ')
