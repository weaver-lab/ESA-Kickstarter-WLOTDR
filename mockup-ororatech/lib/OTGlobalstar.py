#!/usr/bin/env python
#
# Copyright (c) 2019, OroraTech.
#

from STX3 import STX3

maximum_packet_length = 4

class OTGlobalstar:
    stx3 = STX3()
    cue = []

    def __init__(self):
        pass

    # send longer message
    def send(self, message):
        for i in range(0,len(message),maximum_packet_length):
            self.cue.append(message[i:i + maximum_packet_length])

        while(len(self.cue) > 0):
            self.stx3.send_blocking(self.cue.pop(0))
    
    def get_cueLength(self):
        return len(self.cue)