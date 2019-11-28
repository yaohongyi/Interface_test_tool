#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

import sys
import logging
from public import public_method
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from public.interface_request import InterfaceRequest


class Client(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''窗口绘制'''
        self.setFixedSize(1200, 600)
        self.setWindowTitle('接口测试工具_都君_V0.1')
        self.setWindowIcon(QtGui.QIcon('./picture/公鸡.png'))
        self.client_grid = QGridLayout(self)
        # 【请求信息】分组框元素
        self.request_group_box = QGroupBox('【请求信息】')
        self.client_grid.addWidget(self.request_group_box, 0, 0, 9, 1)
        self.http_protocol_label = QLabel('请求协议：')
        self.http_protocol_combo_box = QComboBox()
        self.http_protocol_combo_box.addItems(['http', 'https'])
        self.request_method_label = QLabel('请求方法：')
        self.request_method_combo_box = QComboBox()
        self.request_method_combo_box.addItems(['post', 'get'])
        self.ip_label = QLabel('域名或IP：')
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('请输入域名或者ip')
        self.port_label = QLabel('端口：')
        self.port_input = QLineEdit()
        # 设置端口整型校验
        port_validator = QtGui.QIntValidator()
        port_validator.setRange(0, 65535)
        self.port_input.setValidator(port_validator)
        self.port_input.setPlaceholderText('请输入端口')
        self.path_label = QLabel('请求接口：')
        self.path_combo_box = QComboBox()
        interface_name_list = public_method.get_interface_name_list()  # 通过excel读取下拉框可选项
        interface_name_list.insert(0, '自定义')
        self.path_combo_box.addItems(interface_name_list)
        self.path_combo_box.currentIndexChanged.connect(self.interface_option_change)
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText('请输入路径')
        self.request_time_label = QLabel('请求次数：')
        self.request_time_spin_box = QSpinBox()
        self.request_time_spin_box.setRange(1, 10000)
        self.request_interval_label = QLabel('请求间隔(秒)：')
        self.request_interval_spin_box = QSpinBox()
        self.request_interval_spin_box.setRange(0, 1000)
        self.parameter_label = QLabel('请求参数：')
        self.parameter_text_edit = QPlainTextEdit()
        self.parameter_text_edit.setPlaceholderText('非自定义接口的请求参数可以在Excel文件中进行配置')
        # 【请求信息】分组框布局
        self.request_grid = QGridLayout(self.request_group_box)
        self.request_grid.addWidget(self.http_protocol_label, 0, 0, 1, 1)
        self.http_protocol_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.request_grid.addWidget(self.http_protocol_combo_box, 0, 1, 1, 1)
        self.request_grid.addWidget(self.request_method_label, 0, 2, 1, 1)
        self.request_method_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.request_grid.addWidget(self.request_method_combo_box, 0, 3, 1, 1)
        self.request_grid.addWidget(self.ip_label, 0, 4, 1, 1)
        self.ip_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.request_grid.addWidget(self.ip_input, 0, 5, 1, 1)
        self.request_grid.addWidget(self.port_label, 0, 6, 1, 1)
        self.port_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.request_grid.addWidget(self.port_input, 0, 7, 1, 1)
        self.request_grid.addWidget(self.path_label, 1, 0, 1, 1)
        self.path_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.request_grid.addWidget(self.path_combo_box, 1, 1, 1, 1)
        self.request_grid.addWidget(self.path_input, 1, 2, 1, 6)
        self.request_grid.addWidget(self.request_time_label, 2, 0, 1, 1)
        self.request_grid.addWidget(self.request_time_spin_box, 2, 1, 1, 1)
        self.request_grid.addWidget(self.request_interval_label, 2, 2, 1, 1)
        self.request_grid.addWidget(self.request_interval_spin_box, 2, 3, 1, 1)
        self.request_grid.addWidget(self.parameter_label, 3, 0, 1, 1)
        self.request_grid.addWidget(self.parameter_text_edit, 3, 1, 1, 7)
        # 按钮分组框
        self.button_group_box = QGroupBox()
        self.client_grid.addWidget(self.button_group_box, 9, 0, 1, 1)
        self.send_button = QPushButton('发起请求(F10)')
        self.send_button.setShortcut('F10')
        self.send_button.clicked.connect(self.request_action)
        self.save_button = QPushButton('保存信息(Ctrl+S)')
        self.save_button.setShortcut('Ctrl+S')
        self.clear_button = QPushButton('清空日志(Ctrl+L)')
        self.clear_button.setShortcut('Ctrl+L')
        self.clear_button.clicked.connect(self.clear_action)
        # 按钮分组框布局
        self.button_grid = QGridLayout(self.button_group_box)
        self.button_grid.addWidget(self.send_button, 0, 0)
        self.button_grid.addWidget(self.save_button, 0, 1)
        self.button_grid.addWidget(self.clear_button, 0, 2)
        # 【响应信息】分组框元素
        self.response_group_box = QGroupBox('【日志打印】')
        self.client_grid.addWidget(self.response_group_box, 0, 1, 10, 1)
        self.response_text = QTextBrowser()
        # 【响应信息】分组框布局
        self.response_grid = QGridLayout(self.response_group_box)
        self.response_grid.addWidget(self.response_text)
        # 设置界面字段值初始值
        self.set_default()

    def set_default(self):
        """"""
        ip, port = public_method.get_ip_port()
        self.ip_input.setText(ip)
        self.port_input.setText(port)

    def interface_option_change(self):
        """"""
        interface_option = self.path_combo_box.currentText()
        if interface_option != '自定义':
            # 读取excel
            interface_info = public_method.read_excel(interface_option)
            # 设置接口协议
            protocol = interface_info.get('protocol')
            self.http_protocol_combo_box.setCurrentText(protocol)
            # 设置path_input不可编辑
            self.path_input.setEnabled(False)
            # 设置请求方法
            request_method = interface_info.get('method')
            self.request_method_combo_box.setCurrentText(request_method)
            # 设置接口请求路径
            path = interface_info.get('path')
            self.path_input.setText(path)
            # 设置请求参数
            parameter = public_method.get_request_parameter(interface_info)
            self.parameter_text_edit.setPlainText(str(parameter))
        else:
            self.path_input.setEnabled(True)
            self.path_input.clear()
            self.parameter_text_edit.clear()

    def get_window_info(self) -> dict:
        """
        获取客户端上所有字段的值
        :return: 客户端所有的字段值组成的字典
        """
        protocol = self.http_protocol_combo_box.currentText()
        request_method = self.request_method_combo_box.currentText()
        ip = self.ip_input.text()
        port = self.port_input.text()
        path = self.path_input.text()
        request_time = self.request_time_spin_box.value()
        request_interval = self.request_interval_spin_box.value()
        parameter = self.parameter_text_edit.toPlainText()
        window_info = {
            'protocol': protocol,
            'request_method': request_method,
            'ip': ip,
            'port': port,
            'path': path,
            'request_time': request_time,
            'request_interval': request_interval,
            'parameter': parameter
        }
        window_info_beautify = public_method.format_beautify(window_info)
        logging.debug(f'The window info is：\n{window_info_beautify}')
        return window_info

    @staticmethod
    def join_url(window_info):
        protocol = window_info.get('protocol')
        ip = window_info.get('ip')
        port = window_info.get('port')
        path = window_info.get('path')
        url = f'{protocol}://{ip}:{port}{path}'
        return url

    def request_action(self):
        """发送接口请求"""
        window_info = self.get_window_info()
        url = self.join_url(window_info)
        request_parameter = window_info.get('parameter')
        request_time = window_info.get('request_time')
        request_interval = window_info.get('request_interval')
        self.request_thread = InterfaceRequest(url, eval(request_parameter), request_time, request_interval)
        self.request_thread.text.connect(self.print_action)
        self.request_thread.start()

    def clear_action(self):
        """清空响应消息"""
        self.response_text.clear()

    def save_action(self):
        """保存窗口信息到文件"""
        ...

    def print_action(self, text):
        """"""
        self.response_text.append(text)


def main():
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create('Fusion'))
    client = Client()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
