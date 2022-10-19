import machine
import utime
#Setup the onboard LED Pin as an output
LED = machine.Pin(25,machine.Pin.OUT)
while True:
   LED.value(1)
   utime.sleep(0.5)
   LED.value(0)
   utime.sleep(0.5)
   print("hello world!")