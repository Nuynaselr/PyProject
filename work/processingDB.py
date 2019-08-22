import mysql.connector
from configparser import ConfigParser

def read_db_config(filename='config.ini', section='mysql'):
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
    try:
        data_base = read_db_config()

        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        cursor.execute('SELECT * FROM monitoring_system WHERE UID != "root"')

        array_pid = []
        row = cursor.fetchone()

        while row is not None:
            print(row)
            array_pid.append(row[1])
            row = cursor.fetchone()

        print(array_pid)

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()