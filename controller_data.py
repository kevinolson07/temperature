import time 
from time import sleep 
import serial 
from datetime import datetime
import MySQLdb
# import yaml
# import Adafruit_MAX31855.MAX31855 as MAX31855
import time
import math

mysql = MySQLdb.connect('localhost','root' ,'root','flaskapp')

ser = serial.Serial('/dev/ttyS0', baudrate = 9600, parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
def get_data():
    while 1:
        rx_data = ser.read()
        sleep(0.5)
        data_left = ser.inWaiting()
    
        rx_data += ser.read(data_left)
        #print(rx_data)
        try:
            string_data = rx_data.decode("utf-8")
        except UnicodeDecodeError:
            string_data = "0,0,0,0,0"
        csv_data = string_data.replace(";",",")
        split = csv_data.split(',')
        # print(split)
        # print(split[1])
        try:
            temperature = split[1]
            temperature1 = split[0]
            setpoint = split[2]
            current = split[3]
            pwm = split[4]
        except IndexError:
            temperature = 0
            temperature1 = 0
            setpoint = 0
            current = 0
            pwm = 0
        # final_data = csv_data.replace('\'','')
        ser.write(rx_data)
        class data:
            def __init__ (self):
                self.t1 = temperature
                self.t2 = temperature1
                self.curr = current
                self.pwm = pwm
                self.setpoint = setpoint
        return data()

def log_data(temp1, temp2, curr, pwm, setpoint):
    cur = mysql.cursor()
    print('mysql.cursor executed')
    val = (temp1, temp2, curr, pwm, setpoint)
    cur.execute("INSERT INTO smaug_data(temp_in, temp_out, current, pwm, set_point) VALUES(%s,%s,%s,%s,%s)", val)
    #cur.execute(f"INSERT INTO smaug_data(temp_in,temp_out,current,pwm) VALUES({temp1},{temp2},{curr},{pwm});")
    mysql.commit()
    print("commited the data")

def main():
    var = 0
    while True:
        var +=1
        print(var)
        mysql = MySQLdb.connect('localhost','root' ,'root','flaskapp')
        temp = get_data()
        #print(temp)
        print(temp.t1, temp.t2, temp.curr,temp.pwm,temp.setpoint)
        log_data(temp.t1, temp.t2, temp.curr, temp.pwm,temp.setpoint)
        time.sleep(0.5)
        #print("5 seconds went by")

main()