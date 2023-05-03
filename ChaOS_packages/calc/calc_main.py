from ast import literal_eval
from input import input_float
from colors import print_warning, print_success


def calc_main():
    while True:
        usr_calc = input('calc > ')
        try:
            print_success(f'{usr_calc} =\t{literal_eval(usr_calc)}')
        except Exception:
            print_warning(f'The calculation "{usr_calc}" failed due to illegal input. ')
