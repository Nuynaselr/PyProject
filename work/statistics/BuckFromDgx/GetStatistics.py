import mysql.connector
from configparser import ConfigParser
from os import path
import copy
import csv

data_base = {}
tuple_months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                'October', 'November', 'December')
#exclusive_tables = ['2019_10_12_23_03', '', '']
exclusive_tables = ['2019_10_09_18_50', '2019_10_10_15_57', '2019_10_16_20_51', '2019_11_01_12_00']


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
        read_row = 'SELECT UID FROM ' + name_table + ' GROUP BY UID'

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


def get_data_from_table_CPU(name_table):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        read_json = {}
        read_row = 'SELECT UID, AVG(CPU), AVG(MEM), SUM(ENDTIME - STIME) FROM ' + name_table + ' GROUP BY UID'

        cursor.execute(read_row)
        data_from_db = cursor.fetchall()
        for element in data_from_db:
            read_json[str(element[0])] = [element[1], element[2], element[3]]

        return read_json

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def convert_to_structure_per_month_CPU(list_table):
    # list_user = get_list_user(table)
    data_from_table = []
    for table in list_table:
        data_from_table.append(get_data_from_table_CPU(table))

    final_dict_data = copy.deepcopy(data_from_table[0])

    for element in data_from_table:
        for element_dictionary in element.keys():
            if element_dictionary in final_dict_data:
                final_dict_data.get(element_dictionary)[0] += element.get(element_dictionary)[0]
                final_dict_data.get(element_dictionary)[1] += element.get(element_dictionary)[1]
                final_dict_data.get(element_dictionary)[2] += element.get(element_dictionary)[2]
            else:
                final_dict_data[element_dictionary] = [element.get(element_dictionary)[0],
                                                       element.get(element_dictionary)[1],
                                                       element.get(element_dictionary)[2]]

    length_for_avg = len(data_from_table)
    for element in final_dict_data:
        final_dict_data.get(element)[0] /= length_for_avg
        final_dict_data.get(element)[0] = round(final_dict_data.get(element)[0], 3)

        final_dict_data.get(element)[1] /= length_for_avg
        final_dict_data.get(element)[1] = round(final_dict_data.get(element)[1], 3)

        final_dict_data.get(element)[2] = int(final_dict_data.get(element)[2])

    return final_dict_data


def get_data_from_table_GPU(name_table):
    try:
        connect = mysql.connector.connect(host=data_base.get('host'),
                                          database=data_base.get('database'),
                                          user=data_base.get('user'),
                                          password=data_base.get('password'))

        cursor = connect.cursor()
        read_json = {}
        read_row = 'SELECT UID, GPU, GMEM FROM ' + name_table + ' where GPU != \'\' '

        cursor.execute(read_row)
        data_from_db = cursor.fetchall()

        for element in data_from_db:
            element = list(element)
            element[1] = element[1].split('|')

            for value in element[1]:
                if value == '':
                    element[1].remove('')

            element[2] = element[2].split('|')
            
            for value in element[2]:
                if value == '':
                    element[2].remove('')

            element[0] = str(element[0])

            if element[0] in read_json:
                for j_el_json in range(0, len(element[2])):
                    read_json.get(element[0])[int(element[1][j_el_json])] += int(element[2][j_el_json])
            else:
                read_json[element[0]] = [0, 0, 0, 0]
                for i_el_json in range(0, len(element[2])):
                    read_json.get(element[0])[int(element[1][i_el_json])] += int(element[2][i_el_json])

        return read_json

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        connect.close()


def convert_to_structure_per_month_GPU(list_table):
    # list_user = get_list_user(table)
    data_from_table = []
    for table in list_table:
        data_from_table.append(get_data_from_table_GPU(table))

    final_dict_data = copy.deepcopy(data_from_table[0])

    for element in range(1, len(data_from_table)):
        for element_dictionary in data_from_table[element].keys():
            if element_dictionary in final_dict_data:
                for j_el_json in range(0, len(data_from_table[element].get(element_dictionary))):
                    final_dict_data.get(element_dictionary)[j_el_json] += \
                        data_from_table[element].get(element_dictionary)[j_el_json]
            else:
                final_dict_data[element_dictionary] = [0, 0, 0, 0]
                for i_el_json in range(0, len(data_from_table[element].get(element_dictionary))):
                    final_dict_data.get(element_dictionary)[i_el_json] += \
                        data_from_table[element].get(element_dictionary)[i_el_json]

    return final_dict_data


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


def create_true_list_table(list_tables):
    true_list_tables = {}
    for element in list_tables:
        split_row = [str(x) for x in element.split('_')]
        if split_row[1] in true_list_tables and element not in exclusive_tables:
            true_list_tables.get(split_row[1]).append(element)
        elif element not in exclusive_tables:
            true_list_tables[split_row[1]] = [element]
    return true_list_tables


def write_to_csv(path, table_from_db):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for element_arr_table in table_from_db:
            writer.writerow((str(element_arr_table) + ';UID;CPU(%);MEM(%);TIME(s);GPU0(MB);GPU1(MB);GPU2(MB);GPU3(MB)').split(';'))

            data_about_CPU = convert_to_structure_per_month_CPU(table_from_db.get(element_arr_table))
            data_about_GPU = convert_to_structure_per_month_GPU(table_from_db.get(element_arr_table))
            for element in data_about_CPU:
                if element in data_about_GPU:
                    writer.writerow((' ;' + str(element) + ';' +
                                                            str(data_about_CPU.get(element)[0]) + ';' +
                                                            str(data_about_CPU.get(element)[1]) + ';' +
                                                            str(data_about_CPU.get(element)[2]) + ';' +
                                                            str(data_about_GPU.get(element)[0]) + ';' +
                                                            str(data_about_GPU.get(element)[1]) + ';' +
                                                            str(data_about_GPU.get(element)[2]) + ';' +
                                                            str(data_about_GPU.get(element)[3])).split(';'))
                else:
                    writer.writerow(('' + ';' + (str(element) + ';' +
                                                            str(data_about_CPU.get(element)[0]) + ';' +
                                                            str(data_about_CPU.get(element)[1]) + ';' +
                                                            str(data_about_CPU.get(element)[2]) + ';' +
                                                            '0; 0; 0; 0;')).split(';'))


if __name__ == '__main__':
    path_to_config = path.dirname(path.abspath('')) + '/nparenskiy/config.ini'
    data_base = read_db_config(path_to_config)
    table_from_db = get_list_table()

    # for element_arr_table in table_from_db:
    #     print(element_arr_table)
    #     convert_to_structure_per_month_CPU(table_from_db.get(element_arr_table))

    #data_about_CPU = convert_to_structure_per_month_CPU(['2019_9_12_22_48', '2019_11_18_00_13'])
    #data_about_GPU = convert_to_structure_per_month_GPU(['2019_9_12_22_48', '2019_11_18_00_13'])

    #for element in data_about_CPU:
    #    print('UID: [CPU, MEM, TIME]')
    #    print(element_arr_table)
    #    if element in data_about_GPU:
    #        print('{0}: {1}     {2}'.format(element, data_about_CPU.get(element), data_about_GPU.get(element)))
    #    else:
    #        print('{0}: {1}'.format(element, data_about_CPU.get(element)))
    
    table_from_db = create_true_list_table(table_from_db)
    for element_arr_table in table_from_db:
        print(element_arr_table)
        print('%20s%25s%25s%25s%20s%15s%15s%15s' % ('UID:', 'CPU(%)', 'MEM(%)', 'TIME(s)', 'GPU0(MB)', 'GPU1(MB)', 'GPU2(MB)', 'GPU3(MB)'))
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------')

        data_about_CPU = convert_to_structure_per_month_CPU(table_from_db.get(element_arr_table))
        data_about_GPU = convert_to_structure_per_month_GPU(table_from_db.get(element_arr_table))
        for element in data_about_CPU:
            if element in data_about_GPU:
                print('%20s%25s%25s%25s%20s%15s%15s%15s' % (str(element),
                                                        str(data_about_CPU.get(element)[0]),
                                                        str(data_about_CPU.get(element)[1]),
                                                        str(data_about_CPU.get(element)[2]),
                                                        str(data_about_GPU.get(element)[0]),
                                                        str(data_about_GPU.get(element)[1]),
                                                        str(data_about_GPU.get(element)[2]),
                                                        str(data_about_GPU.get(element)[3])))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------')
            else:
                print('%20s%25s%25s%25s%20s%15s%15s%15s' % (str(element),
                                                        str(data_about_CPU.get(element)[0]),
                                                        str(data_about_CPU.get(element)[1]),
                                                        str(data_about_CPU.get(element)[2]),
                                                        '0', '0', '0', '0'))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    
    write_to_csv(path.dirname(path.abspath('')) + '/nparenskiy/statistics.csv', table_from_db)