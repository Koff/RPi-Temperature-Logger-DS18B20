__author__ = 'fernando'
debug = 1


def read_temp():
    temp = -100
    with open('/sys/bus/w1/devices/28-00000596bf8c/w1_slave') as fp:
        correct_measure = 0
        for line in fp:
            if correct_measure > 0:
                temp = float(line[-6:-2])
                temp /= 100
                if debug > 0:
                    print("Read temperature = " + str(temp))
                    break

            if line[-2] == 'S':
                correct_measure = 1
    return temp


def insert_temp_db(temp):
    import MySQLdb

    db = MySQLdb.connect("localhost", "root", "password", "temps")
    curs = db.cursor()
    curs.execute("INSERT INTO tempdat values(NOW()," + str(temp) + " , '', '')")
    db.commit()
    if debug > 0:
        print("Query: INSERT INTO tempdat values(NOW()," + str(temp) + " , '', '')")
    return 0


tem = read_temp()
if tem > -100:
    insert_temp_db(tem)