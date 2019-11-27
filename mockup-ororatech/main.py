from machine import UART
from OTGlobalstar import OTGlobalstar

sender = OTGlobalstar()


sender.send("123456789")

import pycom
import time
pycom.heartbeat(False)
#while(True):
pycom.rgbled(0x00FF)
time.sleep(1)
pycom.rgbled(0xFF00)
time.sleep(1)
