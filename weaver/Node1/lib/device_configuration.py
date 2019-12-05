# -*- coding: utf-8 -*-
""" Device configuration class for LoPys """
""" Weaver Labs 2019 """

import ubinascii
import pycom
from network import WLAN
import time
def connect_wlan(conf_dict):
    """connect LoPy to local wlan network. see details in ../mesh_config.py"""
    wlan = WLAN(mode=WLAN.STA)
    # don't use static IP
    #wlan.init(mode=WLAN.STA)
    #wlan.ifconfig(config=(conf_dict["ip"],conf_dict["netmask"],conf_dict["gateway"],conf_dict["dns"]))
    if not wlan.isconnected():
        print("Connecting to Wifi...")
        wlan.connect(conf_dict["ssid"],auth=(WLAN.WPA2, conf_dict["password"]), timeout=5000)
    while not wlan.isconnected():
        time.sleep_ms(50)
    print("connected")

def set_mac(mac_id:int):
    """set mac address for 0 - 255 unique devices for LoPy device"""
    if not isinstance(mac_id,int):
        return "mac_id is not an int"

    if not mac_id in range(0,256):
        return "mac_id is not in range"

    with open("/flash/sys/lpwan.ac", "wb") as f:
        mac = bytes([0x00,0x00,0x00,0x00,0x00,0x00,mac_id])
        f.write(mac)

def get_mac()->str:
    """get mac address of LoPy device"""
    return str((ubinascii.hexlify(lora.mac(),':').decode()))

def kill_heartbeat():
    """turn off LED heartbeat"""
    pycom.heartbeat(False)

def led_burst():
    """LED light set to white 4 3 seconds"""
    pycom.rgbled(0x0e355c)
    time.sleep(3)
    pycom.rgbled(0x000000)
