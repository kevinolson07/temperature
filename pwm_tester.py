import time
import RPi.GPIO as GPIO

toggle = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(toggle, GPIO.OUT)

while 1:
    GPIO.output(toggle,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(toggle,GPIO.LOW)
    time.sleep(1)
