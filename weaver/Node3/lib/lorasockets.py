# -*- coding: utf-8 -*-
""" LoRa sockets class """
""" Weaver Labs 2019 """
import socket
import time
import json
import mesh_config as config
import logging_wrapper as lw
from loraserver import LoraSocket
config = config.config

def create_socket(block = False):
    """create a LoRa socket"""
    _obj = LoraSocket()
    s=_obj.get_socket()
    s.setblocking(block)
    return s

def close_socket(socket):
    """close LoRa socket"""
    socket.close()
    return

def send_data(socket,message,number_of_messages):
    #while True:
        for i in range(1,number_of_messages+1):
            data=json.dumps(message[i])
            socket.setblocking(False)
            socket.send(data)
            time.sleep(2)
        return

def recv_data(socket,id):
        time.sleep(1)
        socket.setblocking(True)
        data = socket.recv(230)
        try:
            msg_chunk = json.loads(data)

            return msg_chunk
        except ValueError:
            return None

def message_handler(socket,id):
    message_recv_dict={}
    while True:
        msg_chunk = recv_data(socket,id)

        if msg_chunk is None:
            lw.log_wrap_e1()
            continue

        if not all(keys in msg_chunk for keys in config['key_list']):
            lw.log_wrap_e2()
            continue

        num_of_msgs = int(msg_chunk['num_of_msgs'])
        id_list     = list((range(1,num_of_msgs+1)))
        id_list     = map(str,id_list)

        if msg_chunk['recipient_id'] == id:
            seq_id = msg_chunk['seq_id']
            if seq_id not in message_recv_dict.keys():
                message_recv_dict[seq_id]=msg_chunk['payload']
                if all(idz in message_recv_dict for idz in id_list):
                    return message_recv_dict
