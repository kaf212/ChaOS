import csv


def login():
    # print('test')
    # with open('users.csv', 'a+') as csv_file:
    #     attributes = ['name', 'password']
    #     csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
    #     csv_file.close()

    username = None
    while username is None:
        input_username = input('Username > ')

        with open('users.csv', 'r') as csv_file:
            attributes = ['name', 'password']
            next(csv_file)  # skip attribute header
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

            for line in csv_reader:
                if line['name'] == input_username:
                    username = line['name']
                    password = line['password']

            if username is None:
                print('User not found, try again: ')

    print(f'-- {username} --')
    tries = 3
    while tries > 0:
        input_password = input('Password > ')
        if input_password != password:
            tries -= 1
            print('Wrong password, try again: ')
        else:
            break

    if tries <= 0:
        input('You haven entered too many wrong passwords. ')
        exit()


