import mysql.connector.errors

from ChaOS_pm import install_python_package, import_functions
from colors import print_warning


def cdbms_main():
    print('----------------------------------------------------------')
    print('**** Welcome to the ChaOS Database Management System! ****')
    print('----------------------------------------------------------')

    cnx = None
    inp_database = None
    while cnx is None:
        inp_username = input('Username > ')
        if inp_username == 'exit':
            return None
        inp_password = input('Password > ')
        inp_database = input('Database > ')

        cnx = connect_to_db(inp_username, inp_password, inp_database)

    cursor = cnx.cursor(buffered=True)

    query = None
    while query != 'exit':
        query = input(f'CDBMS [{inp_database}] > ')
        if query == 'exit':
            return None

        try:
            cursor.execute(query)
            print_result(cursor)
        except mysql.connector.errors.ProgrammingError:
            print_warning("Syntax Error")
        except TypeError:
            print_warning("Syntax Error")

    cursor.close()
    cnx.close()


def connect_to_db(username, password, database):
    connector = None
    mysql = None
    try:
        mysql = __import__('mysql')
        errorcode = import_functions('mysql.connector', ['errorcode'])[0]
    except ImportError:
        install_python_package('mysql-connector-python', 'cdbms')
        mysql = __import__('mysql')
        errorcode = import_functions('mysql.connector', ['errorcode'])[0]

    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host='127.0.0.1',
                                      database=database)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
            return None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f'Database "{database}" does not exist.')
            return None
        else:
            print(err)
            return None

    return cnx


def print_result(result_table):
    def print_vertical_separator_line():
        for index, i in enumerate(maximum_field_lengths):
            print('+', end="")
            for j in range(maximum_field_lengths[index] + 2):
                print('-', end="")
        print('+')

    def print_table_header():
        for index, column in enumerate(column_names):
            if len(column) + 2 > maximum_field_lengths[index]:
                maximum_field_lengths[index] = len(column) + 2
        print_vertical_separator_line()
        print("|", end="")
        for index, column in enumerate(column_names):
            for i in range(int( (maximum_field_lengths[index] - len(str(column)))) + 1 ):
                print(" ", end="")
            print(column, end=" |")
        print()

    column_names = [column[0] for column in result_table.description]
    result_table = list(result_table)
    max_record_length = 0
    for record in result_table:  # get the maximum char length of the record set
        charlength = 0
        for value in record:
            charlength += len(str(value))
        if charlength > max_record_length:
            max_record_length = charlength

    maximum_field_lengths = []
    for i in range(len(result_table[0])):
        maximum_field_lengths.append(0)

    for record_1 in result_table:
        for field_index, field in enumerate(record_1):
            if len(str(field)) > maximum_field_lengths[field_index]:
                maximum_field_lengths[field_index] = len(str(field))

    print_table_header()
    print_vertical_separator_line()

    for record in result_table:
        print("|", end="")
        for field_index, field in enumerate(record):
            for i in range(int( (maximum_field_lengths[field_index] - len(str(field)))) + 1 ):
                print(" ", end="")

            print(field, end=" |")

        print("")
    print_vertical_separator_line()

