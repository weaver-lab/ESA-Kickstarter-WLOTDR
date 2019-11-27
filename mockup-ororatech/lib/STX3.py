#!/usr/bin/env python
#
# Copyright (c) 2019, OroraTech.
#

import time

min_burst_intervall = 4      # seconds
debug_initial_waiting_time = 2

class STX3:
    last_burst_time = time.time() - min_burst_intervall + debug_initial_waiting_time
    #uart
    
    def __init__(self): #, rx, tx, rts, cts):
        last_burst_time = time.time() - min_burst_intervall + debug_initial_waiting_time
        #self.uart = UART(0,115200) # TODO uart pins

    # 144 byte message
    def send_blocking(self, message):
        print("STX3 - send - waiting for " + str(self.last_burst_time + min_burst_intervall - time.time() + 1) + " seconds")
        while(time.time() < self.last_burst_time + min_burst_intervall):
            pass
        print("STX3 - send: " + message)
        self.last_burst_time = time.time()
    
    # # check if blocking is necessary
    # def is_available(self):
    #     if time.time() > self.last_burst_time + min_burst_intervall:
    #         return True
    #     else:
    #         return False
    #     self.last_burst_time = time.time()
    
    # # get time until sender is available
    # def timeUntilAvailable(self):
    #     return self.last_burst_time + min_burst_intervall - time.time()