# -*- coding: utf-8 -*-
""" Socket Base Class"""
""" Weaver Labs 2019 """

import socket

class BaseSocket(object):
    """ Base socket class"""
    def __init__(self, sock_type:str, host:str, port:int, protocol:str, sock_id:int, family:str = "AF_INET" ):
        self._type   = type
        self._host   = host
        self._port   = port
        self._id     = sock_id
        self._socket = None
        self._create_socket(family, protocol)

    def _create_socket( self, family:str, protocol:str ) -> None:
        """ Create the required socket based on family and protocol. """
        if protocol == "udp":
            _protocol = socket.SOCK_DGRAM
        elif protocol == "raw":
            _protocol = socket.SOCK_RAW
        else:
            _protocol = socket.SOCK_STREAM
        if family == "AF_INET":
            _family = socket.AF_INET
            self._socket = socket.socket(_family, _protocol)

    def recv( self ) -> bytes:
        """ Receive data from the socket. """
        return self._socket.recv()

    def send(self, data) -> None:
        """ Send data to a connected socket. """
        self._socket.send(data)

    def close(self) -> None:
        """ Close a socket file descriptor. """
        self._socket.close()

    def set_timeout( self, timeout:int ) -> None:
        """ Set a timeout on blocking socket operations. """
        self._socket.settimeout(timeout)

    def set_blocking( self, flag:bool ) -> None:
        """ Set the blocking mode in blocking or non-blocking. """
        self._socket.setblocking(flag)

    def get_type( self ) -> str:
        """ Get socket type. """
        return self._type

    def get_host( self ) -> str:
        """ Get host name. """
        return self._host

    def get_port( self ) -> int:
        """ Get port number. """
        return self._port

    def get_id( self ) -> int:
        """ Get socket id. """
        return self._id

    def get_socket( self ) -> object:
        """ Returns the Lora socket. """
        return self._socket
