# show data in dataBase
def read_data_base():
    data_base = read_db_config()
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        if connect.is_connected():
            print('Connected to MariaDB')

        cursor = connect.cursor()
        cursor.execute("SELECT * FROM monitoring_system")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        connect.close()