import mysql.connector
from configparser import ConfigParser
from os import popen


def gen_element(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD):
    dicti = {
        "UID": UID,
        "PID": PID,
        "PPID": PPID,
        "C": C,
        "SZ": SZ,
        "RSS": RSS,
        "PSR": PSR,
        "STIME": str(STIME),
        "TTY": TTY,
        "TIME": TIME,
        "CMD": CMD
    }
    return dicti


def get_json():
    command = 'ps -eF'
    output = popen(command)
    process = output.read()
    output.close()

    process = process.split('\n')

    for i in range(len(process)):
        process[i] = process[i].split(' ')

    for i in range(len(process)):
        for j in range(process[i].count('')):
            process[i].remove('')

    array_json = []
    process = process[1:]
    for i in range(len(process) - 1):
        if process[i][0] != 'root':
            array_json.append(gen_element(process[i][0], process[i][1], process[i][2], process[i][3],
                                          process[i][4], process[i][5], process[i][6], process[i][7], process[i][8],
                                          process[i][9], process[i][10]))

    return array_json


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


def add_data():
    try:
        data_base = read_db_config()

        query = 'INSERT INTO monitoring_system(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        if connect.is_connected():
            print('Connected to MariaDB')

        data = get_json()
        for cell in data:
            cursor = connect.cursor()
            args = (cell.get('UID'), cell.get('PID'), cell.get('PPID'), cell.get('C'),
                     cell.get('SZ'), cell.get('RSS'), cell.get('PSR'), cell.get('STIME'), cell.get('TTY'),
                     cell.get('TIME'), cell.get('CMD'))


            cursor.execute(query, args)

        # if cursor.lastrowid:
        #     print('last insert id', cursor.lastrowid)
        # else:
        #     print('last insert id not found')

        connect.commit()
        print('Create Table')

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def clean_table():
    try:
        data_base = read_db_config()

        query = 'TRUNCATE TABLE monitoring_system'

        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        if connect.is_connected():
            print('Connected to MariaDB')

        cursor = connect.cursor()
        cursor.execute(query)

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()
        print('Table cleared')


if __name__ == '__main__':
    clean_table()
    add_data()