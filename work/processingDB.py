import mysql.connector
from configparser import ConfigParser
from os import popen
import time

data_base = {}
array_PID = []
array_PID_db = []
name_table = ''
time_sleep = {
    'test': 2,
    'one_minute': 60,
    'two_minutes': 120,
    'three_minutes': 180
}


def gen_element(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD, ENDTIME, LIVE = 'active'):
    dicti = {
        "UID": UID,
        "PID": PID,
        "PPID": PPID,
        "C": C,
        "SZ": SZ,
        "RSS": RSS,
        "PSR": PSR,
        "STIME": time.time(),
        "TTY": TTY,
        "TIME": TIME,
        "CMD": CMD,
        "ENDTIME": ENDTIME,
        "LIVE": LIVE
    }
    return dicti


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


def update_by_pid(PID):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        update_row = 'UPDATE ' + name_table + ' SET ENDTIME = %s WHERE PID = %s'
        cursor.execute(update_row, (time.time(), PID,))

        connect.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()


def update_by_pid_death(PID):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        update_row = 'UPDATE ' + name_table + ' SET LIVE = %s WHERE PID = %s'
        cursor.execute(update_row, ('dead', PID,))

        connect.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()


def read_db():
    json_db = []
    array_PID_db.clear()

    try:
        dbconfig = read_db_config()
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))
        cursor = connect.cursor()
        read_row = "SELECT * FROM " + name_table
        cursor.execute(read_row)

        row = cursor.fetchone()

        while row is not None:
            # print(row)
            json_db.append(gen_element(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                       row[10], row[11], row[12]))
            array_PID_db.append(row[1])
            row = cursor.fetchone()

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()

    return json_db


def get_json():
    array_PID.clear()
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
        if process[i][0] != 'root' and process[i][10] != 'ps' and process[i][10] != '/usr/bin/ps':
            array_json.append(gen_element(process[i][0], process[i][1], process[i][2], process[i][3],
                                          process[i][4], process[i][5], process[i][6], process[i][7], process[i][8],
                                          process[i][9], process[i][10], ''))
            array_PID.append(int(process[i][1]))
    return array_json


def add_data(cell):
    try:
        query = 'INSERT INTO ' + name_table + '(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD, LIVE) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        args = (cell.get('UID'), cell.get('PID'), cell.get('PPID'), cell.get('C'),
                cell.get('SZ'), cell.get('RSS'), cell.get('PSR'), cell.get('STIME'), cell.get('TTY'),
                cell.get('TIME'), cell.get('CMD'), cell.get('LIVE'))


        cursor.execute(query, args)

        # if cursor.lastrowid:
        #     print('last insert id', cursor.lastrowid)
        # else:
        #     print('last insert id not found')

        connect.commit()

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def processing(json, json_db):
    len_json = len(json)
    len_json_db = len(json_db)

    for index in range(len_json if len_json > len_json_db else len_json_db):
        if index < len_json_db:
            if json_db[index].get('PID') in array_PID: #and json_db[index].get('ENDTIME') == None:
                update_by_pid(json_db[index].get('PID'))
            else:
                update_by_pid_death(json_db[index].get('PID'))
        if index < len_json:
            if int(json[index].get('PID')) not in array_PID_db:
                print('add: ', json[index].get('PID'), ' ', json[index])
                add_data(json[index])
            else:
                update_by_pid_death(json_db[index].get('PID'))

    # except IndexError as e:
    #     print(e)
    #     print(error_index)





if __name__ == '__main__':
    try:
        data_base = read_db_config()
        name_table = data_base.get('last_name_table')
        while True:
            processing(get_json(), read_db())
            time.sleep(time_sleep.get('test'))
    except KeyboardInterrupt as er:
        pass
