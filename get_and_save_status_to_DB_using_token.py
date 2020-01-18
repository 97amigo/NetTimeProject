import requests
import time
import datetime
import sqlite3

MyApp_token = 'a6de38cca6de38cca6de38cc59a6b2cd9daa6dea6de38ccfb5d605de0f5d1534cc21f18'
v = 5.92

tokens_List = [MyApp_token]


def putStatusToDB(token):
    current_date = str(datetime.datetime.now())[0:10]
    conn = sqlite3.connect("{}.db".format(current_date))
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE times (time text, status text)""")
    try:
        while True:
            if current_date != str(datetime.datetime.now())[0:10]:
                conn.commit()
                current_date = str(datetime.datetime.now())[0:10]
                conn = sqlite3.connect("{}.db".format(current_date))
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE times (time text, status text)""")

            r = requests.get('https://api.vk.com/method/users.get', params={'user_ids': 112125332, 'fields': 'online',
                                                                            'access_token': token, 'v': v})
            response = r.json()
            values = '{}\', \'{}'.format(str(datetime.datetime.now()), response['response'][0]['online'])
            cursor.execute('INSERT INTO times VALUES (\'{}\')'.format(values))
            time.sleep(120)
    except Exception:
        print('Fucked up...')
    finally:
        conn.commit()
        conn.close()


for i in range(len(tokens_List)):
    putStatusToDB(tokens_List[i])
