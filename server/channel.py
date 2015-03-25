#!/usr/bin/python
# -*- coding:utf-8 -*-
import types
import Queue
from handler import Handler


class Channel(object):
    def __init__(self, server, client, next):
        self.server = server
        self.client = client
        self.next = next

    def input(self, data):
        pass

    def output(self):
        pass


class LineChannel(Channel):
    """
    保存客户端连接
    """

    def __init__(self, server, client, next):
        super(LineChannel, self).__init__(server, client, next)
        self.input_buffer = ''
        self.output_queue = Queue.Queue()

    def input(self, request):
        if '\n' not in request:
            self.input_buffer += request
        else:
            msgs = request.split('\n')
            msg = (self.input_buffer + msgs[0]).strip()
            if msg:
                self.input_buffer = ''
                self.next.input(msg)
            for msg in msgs[1:-1]:
                msg = msg.strip()
                if msg:
                    self.next.input(msg)
            msg = msgs[-1]
            if msg:
                self.input_buffer = msg.strip()

    def output(self):
        return self.next.output()