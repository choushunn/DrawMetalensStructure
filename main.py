"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : main.py
# @Author     : Spring
# @Time       : 10/04/2024 17:27
# @Description:
"""
from draw_structure import draw_structure
from utils import check_dirs, check_requirements


def main():
    check_dirs()
    check_requirements()
    print('开始绘制结构............')
    # 修改数据文件名
    data_file_name = 'data/Data_Lens_3cm_60fs_error0-3_error0-5_5wavelengths_inpolar_metalens4-3(lam4rightdown)-20240402.mat'
    draw_structure(data_file_name)


if __name__ == '__main__':
    main()
