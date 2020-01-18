import urllib.request
import datetime
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

current_date = str(datetime.datetime.now())[0:10]       # текущая дата (год плюс число)
conn = sqlite3.connect("{}.db".format(current_date))    # создание базы данных с одноимённым названием
cursor = conn.cursor()

# Создаём таблицу, куда пишем всю активность пользователся
# на протяжении суток (онлайн/не онлайн)

cursor.execute("""CREATE TABLE times (time text, status text)""")

x = np.array([])        # для хранения временных значений
y = np.array([])        # для хранения статуса

plt.ion()
start_rec_time = str(datetime.datetime.now())[5:10]
plt.title('Начало записи: ' + start_rec_time)

x = np.append(x, str(datetime.datetime.now())[8:16])
y = np.append(y, 0)
plt.plot(x, y)
plt.draw()

try:
    while True:

        # Если текущая дата сменилась(наступили следующие сутки) создаётся новая БД, таблица в ней
        # и запись продолжается уже туда

        if current_date != str(datetime.datetime.now())[0:10]:
            conn.commit()
            current_date = str(datetime.datetime.now())[0:10]
            conn = sqlite3.connect("{}.db".format(current_date))
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE times (time text, status text)""")

            x = np.array([])
            y = np.array([])
            start_rec_time = str(datetime.datetime.now())[5:10]
            plt.title('Начало записи: ' + start_rec_time)

        # Статус извлекаем из скачанной странички

        f = urllib.request.urlopen('https://vk.com/klochook').read()
        index_of_interest_string = f.decode('utf-8').find('<span class="pp_last_activity_text">')
        if f.decode('utf-8')[index_of_interest_string + 36: index_of_interest_string + 42] == 'Online':
            isOnline = '1'      # человек онлайн
        else:
            isOnline = '0'      # человек не онлайн

        time = str(datetime.datetime.now())[11:16]    # текущее время

        x = np.append(x, time)
        y = np.append(y, int(isOnline))

        plt.clf()                       # обновление графика
        plt.pause(0.3)

        plt.title('Начало записи: ' + start_rec_time)
        plt.plot(x, y)
        plt.draw()                  # вывод результатов на графике в реальном времени
        plt.pause(75)               # интервал, с которым происходит запрос

        values = '{}\', \'{}'.format(time, isOnline)
        print(values)
        cursor.execute('INSERT INTO times VALUES (\'{}\')'.format(values))  # сохранение в БД
except Exception:
    print('Fucked up...')
finally:
    conn.commit()
    conn.close()
    plt.ioff()
