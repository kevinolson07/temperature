import MySQLdb
import yaml
import Adafruit_MAX31855.MAX31855 as MAX31855
import time
import math
import csv

mysql = MySQLdb.connect('localhost','root' ,'root','flaskapp')


cur = mysql.cursor()
cur.execute(f"SELECT * FROM smaug_data ORDER BY timestamp ASC;")
data = cur.fetchall()
#mysql.connection.commit()
c = csv.writer(open('controller_TC.csv', 'w'))
for x in data:
    c.writerow(x)