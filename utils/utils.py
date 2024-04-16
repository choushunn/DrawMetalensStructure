"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : utils.py
# @Author     : Spring
# @Time       : 10/04/2024 22:18
# @Description: 
"""
import os

import numpy as np
import scipy.io as sio

from datetime import datetime


def check_dirs():
    """
    检查项目所需文件夹是否存在，不存在则创建
    """
    dirs = ['output', 'data', 'logs']
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
    Beta = data.get('Beta_ij', None)
    structure = data.get('structure', None)
    return {
        'X': X,
        'Y': Y,
        'L': L,
        'W': W,
        'structure': structure,
        'Beta': Beta
    }


def create_filename():
    """
    创建文件名
    :return:
    """
    now = datetime.now()

    timestamp = now.strftime("%Y%m%d_%H%M%S")

    return f"output/{timestamp}.gds"


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


def radians_to_degrees(radians):
    degrees = radians * (180 / np.pi)
    return degrees


if __name__ == '__main__':
    check_dirs()
