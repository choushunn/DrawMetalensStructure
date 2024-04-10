"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : utils.py
# @Author     : Spring
# @Time       : 10/04/2024 22:18
# @Description: 
"""
import os
import scipy.io as sio
import subprocess

from datetime import datetime


def check_dirs():
    """
    检查项目所需文件夹是否存在，不存在则创建
    """
    dirs = ['output', 'data']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)


def read_data(file_name: str):
    """
    读取数据
    :param file_name:
    :return:
    """
    # 判断文件是否存在
    if not os.path.exists(file_name):
        raise FileNotFoundError(f'{file_name} is not exist.')
    data = sio.loadmat(file_name)
    X = data['X'].astype('float')
    Y = data['Y'].astype('float')
    L = data['L'].astype('float')
    W = data['W'].astype('float')
    structure = data['structure']
    return {
        'X': X,
        'Y': Y,
        'L': L,
        'W': W,
        'structure': structure
    }


def create_filename():
    """
    创建文件名
    :return:
    """
    now = datetime.now()

    timestamp = now.strftime("%Y%m%d_%H%M%S")

    return f"output/{timestamp}.gds"


def check_requirements():
    """
    检查依赖是否存在
    :return:
    """
    packages = [
        {"name": "klayout", "command": "pip install klayout --upgrade"},
        {"name": "gdsfactory", "command": 'pip install "gdsfactory[full]" --upgrade'}
    ]

    print("正在检查环境依赖...")
    for package in packages:
        try:
            # 尝试导入包，如果导入成功则已安装
            __import__(package["name"])
            print(f"{package['name']} 已安装")
        except ImportError:
            print(f"{package['name']} 未安装，正在尝试安装...")
            # 执行安装命令
            try:
                subprocess.check_call(package["command"], shell=True)
                print(f"{package['name']} 安装成功")
            except subprocess.CalledProcessError:
                print(f"{package['name']} 安装失败")


def get_radius_width(outer_radius, inner_radius):
    """
    计算半径和宽度
    :param outer_radius:(2*radius+width)/2
    :param inner_radius:(2*radius-width)/2
    :return:
    """
    radius = (outer_radius + inner_radius) / 2
    width = outer_radius - inner_radius
    return radius, width


if __name__ == '__main__':
    check_dirs()
    check_requirements()
