from thermalprinter import *
import time
from time import sleep

printer = ThermalPrinter("/dev/ttyUSB0")
start = time.localtime(time.time())
print(" Intial Start time is\n", start)
printer.out("Intial Start time is\n", start)
printer.out("Hello World\n")
print ("Hello World\n")
end = time.localtime(time.time())
print ("End time is\n", end)
printer.out ("End time is\n", end)
sleep(40)

    
    
    
    
    
