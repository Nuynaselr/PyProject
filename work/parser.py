from os import popen
import json
import time

command = 'ps -eF'
time_sleep = [60, 120, 180]


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


if __name__ == '__main__':

    while True:
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
            array_json.append(gen_element(process[i][0], process[i][1], process[i][2], process[i][3],
                                          process[i][4], process[i][5], process[i][6], process[i][7], process[i][8],
                                          process[i][9], process[i][10]))

        my_json = {
            'item': array_json
        }

        with open("data_file.json", "w") as write_file:
            json.dump(my_json, write_file)

        print(json.dumps(my_json, sort_keys=True, indent=4))
        print("------------------------------------------------------------------------------------------------------")
        time.sleep(time_sleep[0])

"""
{
    [
        {
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
        }, 
        ...
    ]
}
"""