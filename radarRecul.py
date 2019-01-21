#made by Gregory&Valentin for MOS

#import all necessary doc
import RPi.GPIO as GPIO
import lcddriver
import time

#setup for GPIO
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#define all GPIO
TRIG = 4
ECHO = 18
GREEN = 10
YELLOW = 9
RED = 11
BuzzerPin = 26

#named equipment connected to GPIO
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(BuzzerPin,GPIO.OUT)

#setup lcd screen
lcd = lcddriver.lcd()
lcd.lcd_clear()

#functions defining what happens when lights are on
def green_light():
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.LOW)
def yellow_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(RED, GPIO.LOW)
def red_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.HIGH)

#functions for active buzzer
def setup(pin):
    GPIO.output(BuzzerPin, GPIO.LOW)
    GPIO.output(BuzzerPin, GPIO.HIGH)
def on():
    GPIO.output(BuzzerPin, GPIO.HIGH)
def off():
    GPIO.output(BuzzerPin, GPIO.LOW)
def beep(x):
    on()
    time.sleep(x/100)
    off()
    time.sleep(x/100)

#functions for ultrasound detector
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    #distance will be given in cm
    distance = sig_time / 0.000058
    return distance

#loop
while True:
    distance = get_distance()
    time.sleep(0.10)

    if distance >= 40:
        green_light()
        off()
        lcd.lcd_display_string("tout va bien,   ", 1)
        lcd.lcd_display_string("t'es loin...    ", 2)
    elif 40 > distance > 30:
        yellow_light()
        beep(distance)
        lcd.lcd_display_string("La t'avances    ", 1)
        lcd.lcd_display_string("et c'est large  ", 2)
    elif 30 > distance > 20:
        yellow_light()
        beep(distance)
        lcd.lcd_display_string("T'es proche     ", 1)
        lcd.lcd_display_string("alors fais gaffe", 2)
    elif 20 > distance > 10:
        yellow_light()
        beep(distance)
        lcd.lcd_display_string("Alors attention ", 1)
        lcd.lcd_display_string("faudrais freiner", 2)
    elif distance <= 10:
        red_light()
        on()
        lcd.lcd_display_string("HEY STOP TU     ", 1)
        lcd.lcd_display_string("VAS TOUT CASSER!", 2)
#thx for using
