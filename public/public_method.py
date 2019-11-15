#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import os
import configparser
import json
import xlrd
import logging
import requests


def get_project_name():
    """
    获得当前项目名称
    :return: 项目名称
    """
    sep = str(os.sep)
    current_file_path = os.path.split(os.path.abspath(__file__))[0]
    path_split = current_file_path.split(sep)
    name = path_split[2]
    return name


project_name = get_project_name()


def get_log_path(file_name='interface_test.log'):
    """
    获得日志文件保存路径
    :param file_name: 日志文件名称
    :return: 日志文件绝对路径
    """
    sep = str(os.sep)
    current_file_path = os.path.split(os.path.abspath(__file__))[0]
    path_split = current_file_path.split(sep)
    project_index = path_split.index(project_name)
    need_path = path_split[:project_index + 1]
    need_path.append(file_name)
    finally_path = sep.join(need_path)
    return finally_path


def log_config():
    log_path = get_log_path()
    root_logger = logging.getLogger()
    root_logger.setLevel('INFO')
    basic_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(basic_format, date_format)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)
    root_logger.addHandler(sh)
    root_logger.addHandler(fh)


log_config()


def get_config_path(file_name='config.ini'):
    """
    获得config.ini文件路径
    :param file_name: 配置文件名称
    :return: 配置文件绝对路径
    """
    sep = str(os.sep)
    current_file_path = os.path.split(os.path.abspath(__file__))[0]
    path_split = current_file_path.split(sep)
    project_index = path_split.index(project_name)
    need_path = path_split[:project_index + 1]
    need_path.append('config')
    need_path.append(file_name)
    finally_path = sep.join(need_path)
    return finally_path


config_file_path = get_config_path()


def read_config(section, key) -> str:
    """
    读取ini文件中的信息
    :param section: 章节
    :param key: 关键字
    :return: key对应的value
    """
    cf = configparser.ConfigParser()
    cf.read(config_file_path, encoding='utf-8-sig')
    value = cf.get(section, key)
    return value


def get_ip_port():
    ip = read_config('server_info', 'ip')
    port = read_config('server_info', 'port')
    return ip, port


def get_excel_path(file_name='interface_config.xlsx'):
    """
    获得excel文件绝对路径
    :param file_name: excel文件名称
    :return: excel文件绝对路径
    """
    sep = str(os.sep)
    current_file_path = os.path.split(os.path.abspath(__file__))[0]
    path_split = current_file_path.split(sep)
    project_index = path_split.index(project_name)
    need_path = path_split[:project_index + 1]
    need_path.append('config')
    need_path.append(file_name)
    finally_path = sep.join(need_path)
    return finally_path


excel_path = get_excel_path()


def read_excel(interface_name, sheet_name='接口配置') -> dict:
    """
    读取excel信息
    :param interface_name: 接口名称
    :param sheet_name: sheet名称
    :return: 整行数据
    """
    excel = xlrd.open_workbook(excel_path)
    sheet = excel.sheet_by_name(sheet_name)
    case_title_list = sheet.col_values(1)
    row_num = case_title_list.index(interface_name)
    row_value = sheet.row_values(row_num)
    excel_data = {
        'interface_name': row_value[0],
        'describe': row_value[1],
        'protocol': row_value[2],
        'method': row_value[3],
        'path': row_value[4],
        'parameter': row_value[5],
        'relevance_interface': row_value[6],
        'relevance_parameter': row_value[7]
    }
    return excel_data


def get_interface_name_list(sheet_name='接口配置') -> list:
    """
    获取excel中的接口中文名列表
    :param sheet_name: sheet页名称
    :return: 接口中文名列表
    """
    excel = xlrd.open_workbook(excel_path)
    sheet = excel.sheet_by_name(sheet_name)
    interface_name_list = sheet.col_values(colx=1, start_rowx=1)
    return interface_name_list


def str_to_dict(str_object) -> dict:
    """
    将字符串形式的字典转化成字典
    :param str_object: 字符串对象
    :return: 字典对象
    """
    try:
        dict_object = eval(str_object)
    except Exception as reason:
        logging.error(reason)
        dict_object = f'Excel文件请求参数中：{reason}！'
    return dict_object


def get_request_parameter(interface_info):
    """
    获取excel中的请求参数
    :param interface_info: excel读取的接口信息
    :return: 接口请求字典
    """
    parameter = str_to_dict(interface_info.get('parameter'))
    return parameter


def format_beautify(dict_object):
    """
    将字典类型数据美化
    :param dict_object: 字典数据
    :return: 美化后的字段数据
    """
    dict_beautify = json.dumps(dict_object, indent=4, ensure_ascii=False, separators=(',', ':'))
    return dict_beautify


def get_relevance_interface(excel_data):
    """"""
    relevance_interface_str = excel_data.get('relevance_interface')
    relevance_interface_list = relevance_interface_str.split('、')
    return relevance_interface_list

def get_relevance_parameter:
    ...

if __name__ == '__main__':
    res = {
        'hasError': False,
        'errorDesc': '',
        'data': [
            {'name': 'lily', 'age': 18},
            {'name': 'lucy', 'age': 19}
        ]
    }
    a = 'hasError'
    b = 'data[0]'
    c = 'data[0].name'
    d = 'data[0].age'