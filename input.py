def input_y_n(prompt):
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = input(prompt).lower()
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
            print(f'Alte, das sind dini Optione: ')

    return user_input


def input_int(prompt):
    while True:
        try:
            user_input = int(input(prompt))
        except ValueError:
            print('Du musch e natürlichi Zahl igeh du Depp (weisch 1, 2, 3 etc. kännsch?). ')
        else:
            break

    return user_input


def input_float(prompt):
    while True:
        try:
            user_input = float(input(prompt))
        except ValueError:
            print('Du musch e Rationali Zahl igeh du Depp (11.38, 42, 3.124 etc.). ')
        else:
            break

    return user_input