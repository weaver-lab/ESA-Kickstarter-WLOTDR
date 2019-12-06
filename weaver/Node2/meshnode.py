# -*- coding: utf-8 -*-
""" Mesh Node Class """
""" Weaver Labs 2019 """

import device_configuration as dc
import mesh_config
import lorasockets as ls
import urequests
import time
import json
import messaging
import logging_wrapper as lw
import mesh_config
config = mesh_config.config

from sys import print_exception

class Mesh():
    "mesh node class"
    def __init__(self):
        self.s_x = ls.create_socket(False)
        self.id = config["id"]
        self.payload_max = config['byte_length']

        if self.id == '1':
            dc.connect_wlan(config["network"])
            dc.kill_heartbeat()
            self.url       = config['url']
            self.s_x       = ls.create_socket(False)
            self.recipient = 2
            self.sender    = 1

        if self.id == '2':
            dc.kill_heartbeat()
            self.s_x       = ls.create_socket(True)
            self.recipient = 3
            self.sender    = 2
            #should disable wlan

        if self.id == '3':
            dc.kill_heartbeat()
            self.s_x       = ls.create_socket(True)
            self.recipient = None
            self.sender    = None
            #should disable wlan


    def node_launch(self,id):
        """launches correct node"""
        if id == '1':
            self.node_1()
        if id == '2':
            self.node_2()
        if id == '3':
            return self.node_3()

    def node_1(self):
        """node 1 GETS the transaction from datarella api @ http://18.184.150.89/api/handover"""
        """and broadcasts for node 2 to receive"""

        time.sleep(5) #required for network interface to boot
        response           = urequests.get(self.url)
        payload            = response.content
        dc.led_burst()     #GET request succesful
        payload_size       = len(payload)

        number_of_messages = (messaging.message_quantity(payload_size,self.payload_max))

        spliced_payload    = messaging.payload_splicer(payload,number_of_messages,self.payload_max)
        message            = messaging.construct_message(self.recipient, self.sender, spliced_payload)
        while True:
            ls.send_data(self.s_x,message,number_of_messages)



    def node_2(self):
        """node 2 lisntens for messages from node 1. upon receipt, node 2 inspects messages"""
        """to identify if they are intended for node 2. once complete set of messages are received"""
        """node 2 broadcasts the messages with the payload for node 3"""
        while True:
            self.s_x.setblocking(True)
            recv_mesg = ls.message_handler(self.s_x,self.id)
            dc.led_burst()
            print("Received: {}".format(recv_mesg))

            self.s_x.setblocking(False)
            payload            = messaging.payload_rebuild(recv_mesg)
            payload_size       = len(payload)
            number_of_messages = (messaging.message_quantity(payload_size,self.payload_max))

            spliced_payload    = messaging.payload_splicer(payload,number_of_messages,self.payload_max)
            message            = messaging.construct_message(self.recipient, self.sender, spliced_payload)
            ls.send_data(self.s_x,message,number_of_messages)

    def node_3(self):
        #returns json of the form:
        # { "signedTx": "0xf901064d808401312d0094811a45062593a5bf0479795759c783b2751f78f180b8a4f81e650a00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000002435303432326335632d303661372d346533612d623534312d636463393862376262343064000000000000000000000000000000000000000000000000000000001ca0edae0a5e565dc79a708a4ed0eaf497bf983095f892b12d14634571bd28ceb36ba045c915c9b28c56a149ab5b11bbd15d940519311e43f822a7579f4238e1db8af7"}
        """node 3 listens for messages from node 2. upon receipt of the set of messages"""
        """node 3 passes the message to main.py where the ororatech simplex terminal can take it"""
        """node 3 listents"""
        while True:
            recv_mesg      = ls.message_handler(self.s_x,self.id)
            payload        = messaging.payload_rebuild(recv_mesg)
            payload        = json.loads(payload)
            dc.led_burst()
            lw.log_wrap_s1(payload,time.localtime())
            return payload
