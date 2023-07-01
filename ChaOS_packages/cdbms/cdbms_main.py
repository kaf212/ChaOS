from ChaOS_pm import install_python_package, import_functions
import os


def cdbms_main():
    print('----------------------------------------------------------')
    print('**** Welcome to the ChaOS Database Management System! ****')
    print('----------------------------------------------------------')

    inp_username = None  # input('Username > ')
    inp_password = None  # input('Password > ')
    inp_database = None  # input('Database > ')

    cnx = connect_to_db(inp_username, inp_password, inp_database)

    cursor = cnx.cursor(buffered=True)

    query = None
    while query != 'exit':
        print('about to prompt query')
        query = input('Query > ')
        cursor.execute(query)

        print_result(cursor)

        input('Press enter to continue...')

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
        cnx = mysql.connector.connect(user='root', password='1234',
                                      host='127.0.0.1',
                                      database='sakila')
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
        for i in range(max_record_length + ((len(result_table[0])) * 2)):  # print vertical separator line
            print('-', end="")
        print("")

    print(type(result_table))
    result_table = list(result_table)
    print(type(result_table))
    max_record_length = 0
    for record in result_table:  # get the maximum char length of the record set
        charlength = 0
        for value in record:
            charlength += len(str(value))
        if charlength > max_record_length:
            max_record_length = charlength
            print(f'new max_record_length = {max_record_length}')


    maximum_field_lengths = []
    for i in range(len(result_table[0])):
        maximum_field_lengths.append(0)

    for record_1 in result_table:
        for field_index, field in enumerate(record_1):
            print(str(field_index))
            if len(str(field)) > maximum_field_lengths[field_index]:
                maximum_field_lengths[field_index] = len(str(field))

        print(maximum_field_lengths)

    print_vertical_separator_line()
    for record in result_table:

        print("|", end="")
        for field_index, field in enumerate(record):
            for i in range(int( (maximum_field_lengths[field_index] - len(str(field)))) + 1 ):
                print(" ", end="")

            print(field, end=" |")

        print("")
    print_vertical_separator_line()

    """
    for i in range(max_char_length + (len(res_tuple) * 2)):
        print('-', end="")
    """



cdbms_main()
