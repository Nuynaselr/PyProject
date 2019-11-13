import mysql.connector
from configparser import ConfigParser
from os import path

data_base = {}


def get_list_table():
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        # if connect.is_connected():
        #     print('Connected to MariaDB')l

        cursor = connect.cursor()
        read_row = 'SHOW TABLES'

        cursor.execute(read_row)
        data_from_db = cursor.fetchall()
        # ddb - data from data base
        change_ddb_table = []
        for element in data_from_db:
            change_ddb_table.append(element[0])
        change_ddb_table = tuple(change_ddb_table)

        return change_ddb_table

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def get_list_user(name_table):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        # if connect.is_connected():
        #     print('Connected to MariaDB')l

        cursor = connect.cursor()
        read_row = 'SELECT USER FROM ' + name_table + ' GROUP BY USER'

        cursor.execute(read_row)
        data_from_db = cursor.fetchall()
        # ddb - data from data base
        change_ddb_user = []
        for user in data_from_db:
            change_ddb_user.append(user[0])
        change_ddb_user = tuple(change_ddb_user)

        return change_ddb_user

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def get_data_from_table(name_table):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        read_row = 'SELECT USER, CPU, MEM, GPU, GMEM, ENDTIME FROM ' + name_table

        cursor.execute(read_row)
        data_from_db = cursor.fetchall()

        return data_from_db

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def convert_to_structure(data_from_table):
    pass


def read_db_config(filename, section='mysql'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


if __name__ == '__main__':
    path_to_config = path.dirname(path.abspath('')) + '/config.ini'
    print(path_to_config)
    data_base = read_db_config(path_to_config)
    table_from_db = get_list_table()
    print(get_data_from_table(table_from_db[0]))
