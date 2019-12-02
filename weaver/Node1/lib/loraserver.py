# -*- coding: utf-8 -*-
""" Lora Socket Class"""

from network    import LoRa
from basesocket import BaseSocket
import socket

REGION = LoRa.EU868

class LoraSocket( BaseSocket ):

    def __init__( self ):
        """ Initialize lora socket. """
        self._set_lora_mode()
        self._socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    def _set_lora_mode( self ) -> None:
        """ Set the Lora device parameters. """
        LoRa(mode=LoRa.LORA, region=REGION)
