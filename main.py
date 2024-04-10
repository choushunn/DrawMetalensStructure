"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : main.py
# @Author     : Spring
# @Time       : 10/04/2024 17:27
# @Description:
"""
import argparse

from draw_structure import draw_structure
from utils import check_dirs, check_requirements


def parse_args():
    opt = argparse.ArgumentParser()
    opt.add_argument('--data_file', type=str,
                     default='data/Data_Lens_3cm_60fs_error0-3_error0-5_5wavelengths_inpolar_metalens4-3(lam4rightdown)-20240402.mat',
                     help='数据文件名')
    opt.add_argument('--show', type=bool, default=False, help='是否显示')
    return opt.parse_args()


def main():
    check_dirs()
    check_requirements()
    print('开始绘制结构............')
    draw_structure(parse_args())


if __name__ == '__main__':
    main()
