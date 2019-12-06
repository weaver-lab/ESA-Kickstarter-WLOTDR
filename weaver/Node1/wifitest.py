import network
import time
# setup as a station
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect('DSN-IoT', auth=(network.WLAN.WPA2, 'orora.tech.orbit.96'))
while not wlan.isconnected():
    time.sleep_ms(50)
print(wlan.ifconfig())

import usocket
ai = usocket.getaddrinfo('18.184.150.89/api/handover', 80)
print(ai)