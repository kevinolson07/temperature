import MySQLdb
import yaml
import Adafruit_MAX31855.MAX31855 as MAX31855
import time
import math


mysql = MySQLdb.connect(host='localhost',user='root' ,passwd='root',db='serverroom')

#Configure GPIOs
CLK = 25
CS = 24
DO = 18

CLK1 = 22
CS1 = 23
DO1 = 17

TC1 = MAX31855.MAX31855(CLK, CS, DO) 
TC2 = MAX31855.MAX31855(CLK1, CS1, DO1) 

def get_data():
	temperature = TC1.readTempC()
	temperature1 = TC2.readTempC()
	if math.isnan(temperature):
		temperature = 0
	if math.isnan(temperature1):
		temperature1 = 0
	class data:
		def __init__ (self):
			self.t1 = temperature
			self.t2 = temperature1
	return data()

def log_data(temp1, temp2):
	cur = mysql.cursor()
	print('mysql.cursor executed')
	val = (temp1, temp2)
	cur.execute("INSERT INTO temperatures(temp1, temp2) VALUES(%s,%s)",val)
	mysql.commit()
	print("commited the data")
	#mysql.close()
	
def main():
	var = 0
	while True:
		var +=1
		print(var)
		mysql = MySQLdb.connect(host='localhost',user='root' ,passwd='root',db='serverroom')
		temp = get_data()
		print(temp.t1, temp.t2)
		log_data(temp.t1, temp.t2)
		time.sleep(15.0)
		print("15 seconds went by")

main()
