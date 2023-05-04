import ast

import simpleeval

from input import input_float
from colors import print_warning, print_success
from ChaOS_pm import install_python_package


def calc_main():
    try:
        eval_sec = __import__(f'simpleeval')
    except ImportError:
        install_python_package('simpleeval', 'calc')
    while True:
        usr_calc = input('calc > ')
        if usr_calc == 'exit':
            break
        SimpleEval = __import__('simpleeval', globals(), locals(), ['SimpleEval'], 0).SimpleEval
        se = SimpleEval()
        try:
            result = se.eval(usr_calc)
            print_success(f'{usr_calc} =\t{result}')
        except (simpleeval.NameNotDefined, SyntaxError, ZeroDivisionError):
            print_warning(f'Calculation failed due to illegal input. ')


"""
tree = ast.parse(usr_calc, mode="eval")
print_success(f'{usr_calc} =\t{eval(compile(tree, filename="", mode="eval"))}')
"""