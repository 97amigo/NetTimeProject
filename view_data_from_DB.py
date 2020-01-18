import datetime
import sqlite3
import matplotlib.pyplot as plt
import numpy as np


names_of_DBs = ['example.db']

x = np.array([])
y = np.array([])


def getDataFromDB(name):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    sql = "SELECT * FROM times"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data


for i in names_of_DBs:
    data = getDataFromDB(i)
    x = np.append(x, [datetime.datetime(int(data[i][0][0:4]), int(data[i][0][5:7]), int(data[i][0][8:10]),
                                        int(data[i][0][11:13]), int(data[i][0][14:16]), int(data[i][0][17:19]))
                  for i in range(len(data))])

    y = np.append(y, [int(data[i][1]) for i in range(len(data))])

plt.plot(x, y)
plt.show()

