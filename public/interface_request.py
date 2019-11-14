#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

from public.public_method import *
from PyQt5 import QtCore


class InterfaceRequest(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, url, request_parameter):
        super().__init__()
        self.url = url
        self.request_parameter = request_parameter
        self.headers = str_to_dict(read_config('headers', 'headers'))

    def post_request(self):
        res = requests.post(self.url, data=json.dumps(self.request_parameter), headers=self.headers).json()
        return res

    def run(self):
        self.post_request()


if __name__ == '__main__':
    d = {'nickname': 'yaocheng', 'passwd': '123456'}
    u = 'http://192.168.0.75:20006/call?id=experts.login&v='
    ir = InterfaceRequest(u, d)
    r = ir.post_request()
    print(r)
