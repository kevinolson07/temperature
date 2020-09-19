import time
import RPi.GPIO as GPIO
import MySQLdb
import Adafruit_MAX31855.MAX31855 as MAX31855
import math


toggle = 6
level = 0
LOW = time.time()
time_HIGH = 0
CLK = 25
CS = 24
DO = 18

TC1 = MAX31855.MAX31855(CLK, CS, DO) 
GPIO.setup(toggle, GPIO.IN)

mysql = MySQLdb.connect(host='localhost',user='root' ,passwd='root',db='serverroom')

def log_data(period, duty, temp):
    cur =mysql.cursor()
    val = (period, duty, temp)
    cur.execute("INSERT INTO OTS_controller (period, duty, temp) VALUES (%s,%s,%s)", val)
    mysql.commit()

def get_temp():
    temperature = TC1.readTempC()
    if math.isnan(temperature):
        temperature = 0
    class data:
        def __init__ (self):
            self.t1 = temperature
    t = data()
    print(t.t1)
    return data()

while 1:
    if (GPIO.input(toggle) == 1 and level == 0):
        HIGH = time.time()
        LOW = HIGH - LOW
        level = 1
        time_LOW = LOW
        period = time_HIGH + time_LOW
        duty = time_HIGH/period
        print("LOW:", LOW)
        print("PERIOD:",period)
        print("Duty Cycle:", duty)
        t = get_temp()
        log_data(period,duty,t.t1)
    elif(GPIO.input(toggle) == 0 and level == 1):
        LOW = time.time()
        HIGH = LOW - HIGH
        time_HIGH = HIGH
        level = 0
        print("HIGH:", HIGH)
        period=0

