#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import os
import configparser
import json
import re

import xlrd
import logging


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
    root_logger.setLevel('DEBUG')
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
    interface_name_list = sheet.col_values(0)
    row_num = interface_name_list.index(interface_name)
    row_value = sheet.row_values(row_num)
    excel_data = {
        'interface_name': row_value[0],
        'describe': row_value[1],
        'protocol': row_value[2],
        'method': row_value[3],
        'path': row_value[4],
        'parameter': row_value[5],
        'extraction': row_value[6]
    }
    logging.info(f'Through interface name <{interface_name}> get excel data is:\n'
                 f'{format_beautify(excel_data)}')
    return excel_data


def get_zh_interface_name_list(sheet_name='接口配置') -> list:
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


def get_variable_info(variable: str):
    variable_info = variable.split('=')
    variable_path = variable_info[1]
    variable_path_info = variable_path.split('.')
    return variable_path_info


def get_variable_value(original_res, node_path_info: list):
    if len(node_path_info) == 0:
        logging.debug(f'最终获取到的节点值为{original_res}。')
        return original_res
    else:
        for node_path in node_path_info:
            logging.debug(f'开始获取{node_path}节点的值！')
            del node_path_info[0]
            # 通过方括号[]判断节点值是否从列表中获取
            reg = r'([0-9]+)'
            find_node = re.search(reg, node_path)
            if find_node:
                # 获取"["括号起始索引位置
                brackets_start_index = find_node.span()[0]
                # 获取节点值列表
                node_name = node_path[:brackets_start_index-1]
                node_value_list = original_res.get(node_name)
                # 从列表中获取指定索引的值
                node_index = int(find_node.group())
                node_value = node_value_list[node_index]
                logging.debug(f'根据节点索引<{node_index}>获取到值为{node_value}。')
            else:
                node_value = original_res.get(node_path, 'error')
            return get_variable_value(node_value, node_path_info)


if __name__ == '__main__':
    test_res = {"hasError":False,"errorDesc":"","data":{"grouplist":[{"groupid":"whQdDYi0vupGY8Yd8c4PrwycVCqCsLJeLhJlKCbC2RF8kRsFMUyAMv51yzqkb8mB","groupname":"管理员"},{"groupid":"F2fHIZ4GYq8awrNF5zxxlTFsZDldxztTK72tD7hu5lvFFKz32AIMVEy2idiAWzTb","groupname":"FE"},{"groupid":"MJOt7J1kevT7HTBA0r0n0Ew2RyT4zhtvmgnPpgKWVjsA9y6wdm0P48w4Yyks41El","groupname":"TEST"},{"groupid":"4NNl3JbmJTGisER9epyi8plJ056kQOi3C2aWR5nEPhPUG6MCGKD2wZNGJBsGX1Oz","groupname":"DEV"},{"groupid":"qbCJyWOBCPe0fsyf2Vb3GDkRsSCCQxRwda3MjZtG0PAmdP1vQqJwCnG9TlLcHMnc","groupname":"abc"},{"groupid":"nTfSB5V1Cl1JXAcESjX9teVxPW5AJBYwYHGA7wS7efFYAxsW1Vso4WhVZ1063nIF","groupname":"销售部"},{"groupid":"Kj10JeFQXpzql4C4fA5YYISqNunEv25V2wNsVPG6mkvUcoCwtbygB0FKeLYBoveW","groupname":"测试分组"},{"groupid":"gKPISDbnwsIzutQzH97igzODy7ADQhFhUTbxaqiqCyPKMmJC78d7ZJzBNALVBqNW","groupname":"都君"},{"groupid":"ijFNYgEcXzk0NaBC0GhGQ27KH3B1vEtpBHokH1uNil1qiHhy6LJMJl3uInMag9Sc","groupname":"后端"},{"groupid":"Via0Q6KxYRlfPVlaaOsTrU5KjtlpH3JuOFRchTb8yEaqZu0TpANSNS1dCyvTcEDX","groupname":"教学版"}]}}
    s = 'groupname=hasError'
    a = get_variable_info(s)
    result = get_variable_value(test_res, a)
