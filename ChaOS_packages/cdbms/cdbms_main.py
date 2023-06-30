from ChaOS_pm import install_python_package

def cdbms_main():

    connector = None
    mysql = None
    try:
        mysql = __import__('mysql')
        connector = __import__('mysql.connector')
    except ImportError:
        install_python_package('mysql-connector-python', 'cdbms')
        mysql = __import__('mysql')
        connector = __import__('mysql.connector')

    cnx = mysql.connector.connect(user='root', password='1234',
                                  host='127.0.0.1',
                                  database='ambatukam')
    cnx.close()


cdbms_main()
