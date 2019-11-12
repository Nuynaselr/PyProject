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
        data_in_db = cursor.fetchall()
        # ddb - data from data base
        change_ddb = []
        for element in data_in_db:
            change_ddb.append(element[0])
        change_ddb = tuple(change_ddb)

        return change_ddb

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


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
    data_from_db = get_list_table()
    print(data_from_db)
