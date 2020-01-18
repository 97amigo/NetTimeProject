from flask import Flask
import io
import base64
import sqlite3
import matplotlib.pyplot as plt
import datetime
import numpy as np

conn = sqlite3.connect("example.db")
cursor = conn.cursor()
sql = "SELECT * FROM times"
cursor.execute(sql)
data = cursor.fetchall()
conn.close()

x = np.array([datetime.datetime(int(data[i][0][0:4]), int(data[i][0][5:7]), int(data[i][0][8:10]),
                                int(data[i][0][11:13]), int(data[i][0][14:16]), int(data[i][0][17:19]))
              for i in range(len(data))])

y = np.array([int(data[i][1]) for i in range(len(data))])

plt.plot(x, y, marker='o')

app = Flask(__name__)


@app.route('/')
def build_plot():

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__ == '__main__':
    app.debug = True
    app.run()
