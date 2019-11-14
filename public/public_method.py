#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import os
import configparser
import json
import xlrd


def get_config_path(project_name='Interface_test_tool', file_name='config.ini'):
    """获得config.ini文件保存路径"""
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


def get_excel_path(project_name='Interface_test_tool', file_name='interface_config.xlsx'):
    """获得excel文件保存路径"""
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
    info = {
        'name': row_value[0],
        'describe': row_value[1],
        'method': row_value[2],
        'path': row_value[3],
        'parameter': row_value[4]
    }
    return info


def get_interface_name_list(sheet_name='接口配置'):
    """获取接口名清单"""
    excel = xlrd.open_workbook(excel_path)
    sheet = excel.sheet_by_name(sheet_name)
    interface_name_list = sheet.col_values(1, -1)
    return interface_name_list


def get_request_parameter(interface_info):
    """
    获取excel中的请求参数
    :param interface_info: excel读取的接口信息
    :return: 接口请求字典
    """
    parameter = eval(interface_info.get('parameter'))
    return parameter


def format_beautify(dict_object):
    """
    将字典类型数据美化
    :param dict_object: 字典数据
    :return: 美化后的字段数据
    """
    dict_beautify = json.dumps(dict_object, indent=4, ensure_ascii=False, separators=(',', ':'))
    return dict_beautify


if __name__ == '__main__':
    result = get_interface_list()
    print(result)
