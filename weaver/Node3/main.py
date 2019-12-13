# -*- coding: utf-8 -*-
""""Main.py for LoPy device"""

import meshnode
import lib.lorasockets as ls
import mesh_config
config = mesh_config.config

node=meshnode.Mesh()
payload = node.node_launch(config['id'])
print("Complete payload received over Lora network: {}".format(payload))
raw_message = payload['signedTx']

print("Transmitting message to satellite...")

from machine import UART, Pin
import time

# TX, RX, RTS, CTS
# Hardware Flow control doesn't work as the default level of RTS and CTS needs to be high
uart1 = UART(1, baudrate=9600, pins=('P20', 'P18'), bits=8, parity=None, stop=1)

rts = Pin('P19', mode=Pin.OUT)
rts.value(1)
cts = Pin('P17', mode=Pin.IN, pull=Pin.PULL_UP)

# remove leading 0x
raw_message = raw_message[2:]
# for testing purposes:
#raw_message = 'f901064d808401312d0094811a45062593a5bf0479795759c783b2751f78f180b8a4f81e650a00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000002435303432326335632d303661372d346533612d623534312d636463393862376262343064000000000000000000000000000000000000000000000000000000001ca0edae0a5e565dc79a708a4ed0eaf497bf983095f892b12d14634571bd28ceb36ba045c915c9b28c56a149ab5b11bbd15d940519311e43f822a7579f4238e1db8af7'

# cut packets (up to 144 data bytes -> 288 characters)
packet_length = 100
packets = []
for i in range(0, len(raw_message), packet_length):
    packets.append(raw_message[i : i + packet_length])

# add packet header
for i in range(len(packets)):
    if len(packets) > 9:
        print("Error: max packet number ( > 9)")
        exit()
    packets[i] = str(i) + str(len(packets)) + packets[i]
print("Number of packets: {}".format(len(packets)))
print(packets)

import device_configuration as dc
import pycom
pycom.heartbeat(False)

# reset STX3
reset_pin = Pin('P8', mode=Pin.OUT)
reset_pin.value(1)
time.sleep(1)
reset_pin.value(0)

# Repeat GLobalstar transmission 10 times
for i in range(10):
    for packet in packets:
        for i in range(1):
            rts.value(0)
            while cts():
                pass
            pycom.rgbled(0x330000)
            print("Sending:  {}".format(packet))
            uart1.write("AT+CMGS=")
            cue = []
            for i in range(0,len(packet),10):
                cue.append(packet[i:i+10])
            for p in cue:
                uart1.write(p)
                time.sleep(0.2)
            uart1.write("\r")
            uart1.wait_tx_done(1000)
            print("Wait for cts high level")
            rts.value(1)
            while cts() == 0:
                pass
            pycom.rgbled(0x003300)
            time.sleep(1)
            print(uart1.readall())
            time.sleep(10)#60 * 5)
    print("Done")
    dc.led_burst()
