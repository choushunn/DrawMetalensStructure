"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : main.py
# @Author     : Spring
# @Time       : 10/04/2024 17:27
# @Description:
"""
import argparse
import cProfile
import pstats

from draw_structure import draw_structure
from utils import check_dirs
from utils.check_env import check_requirements


def parse_args():
    """
    解析命令行参数
    :return:
    """
    opt = argparse.ArgumentParser()
    opt.add_argument('--data_file', type=str,
                     default='data/Data_Lens_3cm_60fs_error0-3_error0-5_5wavelengths_inpolar_metalens4-3(lam4rightdown)-20240402.mat',
                     help='数据文件名')
    opt.add_argument('--show', type=bool, default=False, help='是否显示进度条，绘制大文件时建议不显示')
    # 度量单位
    opt.add_argument('--units', type=float, default=1e-3, help='度量单位，1表示um,1e-3表示nm')
    opt.add_argument('--multiple', type=bool, default=False, help='使用多线程绘制')
    opt.add_argument('--stop_num', type=int, default=-1, help='绘制多少个结构停止,-1为不停止')
    return opt.parse_args()


def main():
    """
    主函数
    :return:
    """
    check_requirements()
    check_dirs()
    print('正在绘制，请等待......')
    draw_structure(parse_args())
    print('绘制完成')


def test():
    """
    性能测试
    :return:
    """
    cProfile.run('draw_structure(parse_args())', filename='logs/profile.log')
    p = pstats.Stats('logs/profile.log')
    # p.strip_dirs().sort_stats(-1).print_stats()
    # 打印累计耗时最多的10个函数
    p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)

    # 打印内部耗时最多的10个函数（不包含子函数）
    p.sort_stats(pstats.SortKey.TIME).print_stats(10)


if __name__ == '__main__':
    main()
    # test()
