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


def add_data(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD):
    try:
        data_base = read_db_config()

        query = 'INSERT INTO monitoring_system(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        args = (UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD)

        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        if connect.is_connected():
            print('Connected to MariaDB')

        cursor = connect.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        connect.commit()

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


if __name__ == '__main__':
    """
         0 "UID": "root",
         1 "PID": 1,
         2 "PPID": 0,
         3 "C": 0,
         4 "SZ": 30299,
         5 "RSS": 9932,
         6 "PSR": 2,
         7 "STIME": "15:31",
         8 "TTY": "?",
         9 "TIME": "00:00:02",
         10 "CMD": "/sbin/init"
     """
    add_data("root", 1, 0, 0, 30299, 9932, 2, "15:31", "?", "00:00:02", "/sbin/init")
