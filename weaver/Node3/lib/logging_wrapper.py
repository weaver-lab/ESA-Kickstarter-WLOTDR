# -*- coding: utf-8 -*-
"""log wrapper library to compensate for micropython's lack of a logging module"""
""" Weaver Labs 2019 """

import time
from sys import print_exception

# SUCCESS
def log_wrap_s1(payload,time):
    with open(file='_logs_success.txt', mode='a+') as f:
        f.write("S1_payload received at_{}\n".format(time))
        return
# ERRORS
#File "/flash/lib/lorasockets.py", line 52, in message_handler #KeyError: num_of_msgs as a result of socket receiving nothing
def log_wrap_e1():
    with open(file='_logs_error.txt', mode='a+') as f:
        f.write("E1_error socket received None @{} \n".format(time.localtime()))
        return

def log_wrap_e2():
    with open(file='_logs_error.txt', mode='a+') as f:
        f.write("E2_error missing key in dict  \n".format(time.localtime()))
        return
