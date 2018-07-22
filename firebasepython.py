#******************************************#
#                  PARKSMART               #
#          shivam.anand936@gmail.com       #
#******************************************#


import RPi.GPIO as GPIO
import time
from pad4pi import rpi_gpio
from threading import Timer
import sys
from firebase import firebase

DEFAULT_KEY_DELAY = 300
DEFAULT_REPEAT_DELAY = 1.0
DEFAULT_REPEAT_RATE = 1.0
DEFAULT_DEBOUNCE_TIME = 200
GPIO.setmode(GPIO.BCM)  
checkkey = 0

#******************************************#
KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

COL_PINS = [17, 15, 14, 25] # BCM numbering
ROW_PINS = [24,22,27,18] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS, key_delay=DEFAULT_KEY_DELAY, repeat=True, repeat_delay=DEFAULT_REPEAT_DELAY, repeat_rate=DEFAULT_REPEAT_RATE)

#******************************************#
f= open('data.txt', 'r')
vehicle = f.read()
firebase=firebase.FirebaseApplication('https://parksmart-shivam.firebaseio.com/')

firebase.post('/user', data={'Vehicle Details': vehicle})
def printKey(key):

    lcd_byte(ord(key),LCD_CHR)
    print(key, end = "")

    if (key == "#"):
       lcd_byte(0x01, LCD_CMD)
       lcd_string(" See you later!",LCD_LINE_1)
       print ("\n\n        See you later !\n\n\n")
       GPIO.cleanup()
       sys.exit()

    
    
#******************************************#

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)




# Define GPIO to LCD mapping
LCD_RS = 21
LCD_E  = 20
LCD_D4 = 26
LCD_D5 = 19
LCD_D6 = 13
LCD_D7 = 6



# Define LCD parameters
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


#******************************************#
def main():
  # Main program block
  global pm
  global system_sts
  
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7


  # Initialise display
  lcd_init()
  lcd_byte(0x01, LCD_CMD)
  lcd_string(" **PARKSMART**",LCD_LINE_1)
  lcd_byte(0xC0, LCD_CMD)
  print ("      **P A R K S M A R T** \n")
  localtime = time.asctime( time.localtime(time.time()))
  print ("In time is: \n", localtime)
  print ("\nVehicle number is: ")
  while (checkkey == 0):
      time.sleep(1)

      
#******************************************#  
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

#******************************************#
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

#******************************************#
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

#***************************************#


def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    

#******************************************#






    

if __name__ == '__main__':
    main()
 
    
