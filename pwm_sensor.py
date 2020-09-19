import time
import RPi.GPIO as GPIO
import MySQLdb
import Adafruit_MAX31855.MAX31855 as MAX31855

toggle = 31
level = 0
counter =0
LOW = time.time()
time_HIGH = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(toggle, GPIO.IN)
mysql = MySQLdb.connect(host='localhost',user='root' ,passwd='root',db='serverroom')

def log_data(period, duty):
    cur =mysql.cursor()
    val = (period, duty)
    cur.execute("INSERT INTO OTS_controller (period, duty) VALUES (%s,%s)", val)
    mysql.commit()

def get_temp():
    

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
        log_data(period,duty)
    elif(GPIO.input(toggle) == 0 and level == 1):
        LOW = time.time()
        HIGH = LOW - HIGH
        time_HIGH = HIGH
        level = 0
        print("HIGH:", HIGH)
        period=0

