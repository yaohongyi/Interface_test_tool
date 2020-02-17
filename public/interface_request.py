#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import requests
from public.public_method import *
from PyQt5 import QtCore


class InterfaceRequest(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, url, request_parameter, request_time=1, request_interval=0):
        super().__init__()
        self.url = url
        self.request_parameter = request_parameter
        self.request_time = request_time
        self.request_interval = request_interval
        self.headers = str_to_dict(read_config('headers', 'headers'))

    def post_request(self):
        """
        通用接口POST请求
        :return: 接口响应
        """
        res = requests.post(self.url, data=json.dumps(self.request_parameter), headers=self.headers).json()
        res_beautify = format_beautify(res)
        req_beautify = format_beautify(self.request_parameter)
        logging.info(f'【请求消息】：\n{req_beautify}')
        logging.info(f'【响应消息】：\n{res_beautify}')
        self.text.emit(f'【请求消息】：\n{req_beautify}')
        self.text.emit('')
        self.text.emit(f'【响应消息】：\n{res_beautify}')
        self.text.emit('')
        self.text.emit('≡' * 35)
        self.text.emit('')
        return res

    def extraction_request(self):
        """
        加强型POST接口请求，增加请求次数、请求时间间隔
        :return: None
        """
        for i in range(self.request_time):
            self.post_request()
            time.sleep(self.request_interval)

    def run(self):
        self.extraction_request()


if __name__ == '__main__':
    d = {'nickname': 'yaocheng', 'passwd': '123456'}
    u = 'http://192.168.0.75:20006/call?id=experts.login&v='
    ir = InterfaceRequest(u, d)
    r = ir.post_request()
