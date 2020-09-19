import time
import RPi.GPIO as GPIO

toggle = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(toggle, GPIO.IN)

level = 0
counter =0
LOW = time.time()
time_HIGH = 0
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
    elif(GPIO.input(toggle) == 0 and level == 1):
        LOW = time.time()
        HIGH = LOW - HIGH
        time_HIGH = HIGH
        level = 0
        print("HIGH:", HIGH)
        period=0
# if 
#     seconds = time.time()
#     time.sleep(1)
#     print(seconds)
#     x=x+1