# -*- coding: utf-8 -*-
"""Messaging Library for LoPy devices"""

from math import ceil
import json

def payload_rebuild(payload_dict):
    """constructs payload upon arrival of all sub-messages"""
    key_list = list(payload_dict.keys())
    key_list = list(map(int, key_list))
    key_list.sort()
    payload=""
    for i in key_list:
            payload = payload + payload_dict[str(i)]
    return payload

def message_quantity(payload_size, max_size):
    """computes # of messages based on size of payload"""
    num_messages = ceil(payload_size / max_size)
    return num_messages

def payload_splicer(payload,number_of_messages,max_size):
    """slices n dices payload in order to encapsulate in message less than LoRa max transmission size. lol"""
    start = 0
    end   = max_size

    payload_spliced_list = []
    for i in range(1,number_of_messages+1):
        payload_spliced_list.append(payload[start:end])
        start = end
        end   = start + max_size
    return payload_spliced_list

def construct_message(recipient, sender, spliced_payload):
    """constructs messages with sliced n' diced payload, recipient id, sender id, seq id and total number of sub-messages """
    message={}
    num_of_messages = len(spliced_payload)

    for index, i in enumerate(spliced_payload):
        index=index+1
        mess_dict = {"recipient_id": str(recipient),
                     "sender"      : str(sender),
                     "seq_id"      : str(index),
                     "num_of_msgs" : str(num_of_messages),
                     "payload"     : i
        }
        message[index]=(mess_dict)
    return message
