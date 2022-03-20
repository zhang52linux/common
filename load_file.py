# _*_ coding: utf-8 _*_
import glob
import inspect
import os
import re

import yaml  # pip install pyyaml


def load_yml(conf_dir) -> dict:
    """ 加载yml文件 """
    with open(file=conf_dir, mode='r', encoding="utf-8") as f:
        return yaml.load(stream=f, Loader=yaml.FullLoader)


def makedirs(dir):
    """ 创建目录 """
    os.makedirs(dir, exist_ok=True)


def get_files_path(search_dir, full_path: bool = True, filter=False):
    """ 获取目录下文件路径
    :param search_dir: 搜索目录路径
    :param full_path: 是否获取完整路径
    :param filter: 正则表达式过滤
    :return 路径列表
    """

    files_path = []

    for dir_path, dir_names, file_names in os.walk(search_dir):
        for file_name in file_names:
            if filter and not re.search(filter, file_name):
                continue
            if full_path:
                files_path.append(os.path.join(dir_path, file_name))
            else:
                files_path.append(file_name)

    return files_path


def read_file_data(file_name) -> str:
    """ 获取文件文本数据 只支持utf-8和gbk编码文件"""

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()
    except UnicodeDecodeError:
        with open(file_name, 'r', encoding='gbk') as f:
            data = f.read()

    return data


def load_yml_conf(conf_dir=None):
    """ 加载目录下所有yml配置 默认从config目录加载 """

    conf = {}
    conf_dir = conf_dir or os.path.join(os.path.dirname(__file__), 'config')
    for file_path in glob.glob(os.path.join(conf_dir, '*.yml')):
        conf_obj = load_yml(file_path)
        conf_name = os.path.splitext(os.path.basename(file_path))[0]
        conf[conf_name] = conf_obj

    return conf


def get_file_name():
    """ 获取当前执行所在文件名 不含后缀 """
    return os.path.basename(inspect.stack()[1][1]).split('.')[0]
