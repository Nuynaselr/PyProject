import mysql.connector
from configparser import ConfigParser
from os import popen
import time

data_base = {}
name_table = str(time.strftime("%Y_%m_%j_%H_%M"))
path_to_config = '/home/np/PyProject/work/config.ini'


def gen_element(UID, PID, PPID, C, SZ, RSS, PSR, TTY, TIME, CMD, PCPU, PMEM, LIVE = '1'):
    time_process = time.time() + 5
    dicti = {
        "UID": UID,
        "PID": PID,
        "PPID": PPID,
        "C": C,
        "SZ": SZ,
        "RSS": RSS,
        "PSR": PSR,
        "STIME": time_process,
        "TTY": TTY,
        "TIME": TIME,
        "CMD": CMD,
        "CPU": float(PCPU),
        "MEM": float(PMEM),
        "GPU": '',
        "GMEM": '',
        "ENDTIME": time_process,
        "LIVE": LIVE
    }
    return dicti


def get_njson():
    # row = ''
    # with open('nvidiaData', 'r') as file:
    #       row = file.read()
    output = popen('nvidia-smi pmon -c 1 -s m')
    row = output.read()
    output.close()

    row = row.split('\n')

    row.pop(0)
    row.pop(0)

    for i in range(len(row)):
        row[i] = row[i].split(' ')

    for i in range(len(row)):
        for j in range(row[i].count('')):
            row[i].remove('')

    array_json = []
    for i in range(len(row) - 1):
        if row[i][0] != 'root':
            array_json.append({
                'GPU': row[i][0],
                'PID': row[i][1],
                'TYPE': row[i][2],
                'GMEM': row[i][3],
                'COMMAND': row[i][4]
            })
    return array_json


def get_json():
    command = 'ps -eo uid,pid,ppid,c,sz,rss,psr,tty,time,pcpu,pmem,cmd'
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
        if process[i][0] != '0' and process[i][11] != 'ps' and process[i][11] != '/usr/bin/ps':
            array_json.append(gen_element(process[i][0], process[i][1], process[i][2], process[i][3],
                                          process[i][4], process[i][5], process[i][6], process[i][7],
                                          process[i][8], process[i][11], process[i][9], process[i][10]))

    array_njson = get_njson()
    for element in array_json:
        for element_n in array_njson:
            if element.get('PID') == element_n.get('PID'):
                element.update({'GPU': str(element.get('GPU')) + '|' + element_n.get('GPU')})
                element.update({'GMEM': str(element.get('GMEM')) + '|' + element_n.get('GMEM')})
                element.update({'TYPE_': element_n.get('TYPE')})

    return array_json


def read_db_config(filename=path_to_config, section='mysql'):
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


def create_table():
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        # if connect.is_connected():
        #     print('Connected to MariaDB')l

        cursor = connect.cursor()
        create_row = 'CREATE table %s ' \
                     '(UID INTEGER , ' \
                     'PID INTEGER, ' \
                     'PPID INTEGER, ' \
                     'C INTEGER, ' \
                     'SZ INTEGER, ' \
                     'RSS INTEGER, ' \
                     'PSR INTEGER, ' \
                     'STIME VARCHAR(20), ' \
                     'TTY VARCHAR(10), ' \
                     'TIME VARCHAR(8), ' \
                     'CMD VARCHAR(70), ' \
                     'CPU DOUBLE (4,1), ' \
                     'MEM DOUBLE (4,1), ' \
                     'GPU VARCHAR (10), ' \
                     'TYPE_ varchar (1), ' \
                     'GMEM varchar (10), ' \
                     'ENDTIME VARCHAR(20), ' \
                     'LIVE VARCHAR(7), ' \
                     'PRIMARY KEY (PID) )' % name_table

        cursor.execute(create_row)
    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def add_data():
    try:
        query = 'INSERT INTO ' + name_table + '(UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD, CPU, MEM, GPU, TYPE_, GMEM, ENDTIME, LIVE) ' \
                                              'VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        # if connect.is_connected():
        #     print('Connected to MariaDB')

        data = get_json()
        for cell in data:
            cursor = connect.cursor()
            args = (cell.get('UID'), cell.get('PID'), cell.get('PPID'), cell.get('C'),
                     cell.get('SZ'), cell.get('RSS'), cell.get('PSR'), cell.get('STIME'), cell.get('TTY'),
                     cell.get('TIME'), cell.get('CMD'), cell.get('CPU'), cell.get('MEM'), cell.get('GPU'),
                    cell.get('TYPE_'), cell.get('GMEM'),cell.get('ENDTIME'), cell.get('LIVE'))


            cursor.execute(query, args)

        # if cursor.lastrowid:
        #     print('last insert id', cursor.lastrowid)
        # else:
        #     print('last insert id not found')

        connect.commit()
        # print('Create Table')

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def spec_main():
    head = []
    row = ''
    with open(path_to_config, 'r') as config:
        head = [next(config) for x in range(5)]

    with open('config.ini', 'w') as config:
        for i in range(5):
            row = row + head[i]
        row = row + 'last_name_table = ' + name_table + '\n'
        config.write(row)

    data_base = read_db_config()
    create_table()
    add_data()


if __name__ == '__main__':
    head = []
    row = ''
    with open(path_to_config, 'r') as config:
        head = [next(config) for x in range(5)]

    with open('config.ini', 'w') as config:
        for i in range(5):
            row = row + head[i]
        row = row + 'last_name_table = ' + name_table + '\n'
        config.write(row)

    data_base = read_db_config()
    create_table()
    add_data()