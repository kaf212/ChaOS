def input_y_n(prompt):
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = input(prompt)
        if user_input not in ['y', 'n']:
            print(f'"{user_input} is not a valid input. Try "y" or "n". ')

    return user_input


def input_selection(valid_selections, selection_names, prompt):
    """
    asks the user for yes or no with a given prompt as question.
    :param selection_names:
    :param valid_selections:
    :param prompt:
    :return user_input:
    """
    while True:
        print(f'{prompt}')
        for selection_name, selection_letter in zip(selection_names, valid_selections):
            print(f'{selection_letter.upper()}) {selection_name}')
        user_input = input('> ').lower()
        if user_input in valid_selections:
            break
        else:
            list_selection_options(user_input, valid_selections)

    return user_input


def list_selection_options(false_user_input: str, valid_selections: list):
    print(f'"{false_user_input}" is not a valid input. Try ', end="")
    i = 0
    reached_end = False
    for sel in valid_selections:
        print(f'"{sel}"', end="")
        if i == len(valid_selections) - 2:
            print(' or ', end="")
            reached_end = True
        elif not reached_end:
            print(', ', end="")
        i += 1
    print('.\n')

def input_int(prompt):
    while True:
        try:
            user_input = int(input(prompt))
        except ValueError:
            print(f'Input is not an integer. ')
        else:
            break

    return user_input


def input_float(prompt):
    while True:
        try:
            user_input = float(input(prompt))
        except ValueError:
            print('Input is not a float. ')
        else:
            break

    return user_input
