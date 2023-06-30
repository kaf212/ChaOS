from ChaOS_pm import install_python_package, import_functions


def cdbms_main():
    print('----------------------------------------------------------')
    print('**** Welcome to the ChaOS Database Management System! ****')
    print('----------------------------------------------------------')

    inp_username = input('Username > ')
    inp_password = input('Password > ')
    inp_database = input('Database > ')

    cnx = connect_to_db(inp_username, inp_password, inp_database)

    cursor = cnx.cursor(buffered=True)
    query = None
    while query != 'exit':
        query = input('Query > ')
        cursor.execute(query)
        print(type(cursor))

        for line in cursor:
            print(line)

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


cdbms_main()
