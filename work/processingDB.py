import mysql.connector
from configparser import ConfigParser
#DELETE from monitoring_system where PID = 747;

data_base = {}


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


def delete_by_pid(PID):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        cursor.execute('DELETE FROM monitoring_system WHERE PID = %s', (PID,))

        connect.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()


def read_db():
    json_db = []

    try:
        dbconfig = read_db_config()
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM books")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            json_db.append(gen_element(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            row = cursor.fetchone()

    except mysql.connector.Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()

    return json_db


if __name__ == '__main__':
    data_base = read_db_config()

