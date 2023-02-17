def input_y_n(prompt):
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = input(prompt).lower()
        if user_input not in ['y', 'n']:
            print(f'"{user_input} is not a valid input. Try "y" or "n". ')

    return user_input
