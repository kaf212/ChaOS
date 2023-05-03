import shutil
from colors import print_warning

AVAILABLE_PACKAGES = {'calc'}


def pm_install(cmd):
    if cmd.sec_arg in AVAILABLE_PACKAGES:
        try:
            shutil.copytree(f'ChaOS_packages/{cmd.sec_arg}', f'A/System42/programs/{cmd.sec_arg}')
        except FileNotFoundError:
            print_warning(f'The system failed to locate resources for package "{cmd.sec_arg}", '
                          f'consider contacting a developer.')



