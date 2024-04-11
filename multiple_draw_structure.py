"""
# -*- coding:utf-8 -*-
# @Project    : main.py
# @FileName   : multiple_draw_structure.py
# @Author     : Spring
# @Time       : 11/04/2024 11:04
# @Description: 
"""
import numpy as np
import gdsfactory as gf
from tqdm import tqdm

from utils import create_filename, read_data, get_radius_width


def draw_structure(opt):
    """
    绘制结构
    :param opt: 输入参数
    :return:
    """
    data = read_data(opt.data_file)
    # 统一单位
    units = opt.units
    # 获取数据
    X, Y, L, W, structure = data['X'], data['Y'], data['L'], data['W'], data['structure']
    # 创建画布
    layout = gf.Component("My_Layout")
    # 计算总结构数
    N = len(X)
    # 计算索引
    indices = np.indices((N, N)).reshape(2, -1).T
    # 计算半径,单位
    r = (np.sqrt(1.8 ** 2 + 1.8 ** 2) + 1.6) * 10 ** 7

    # 初始化进度条
    p_bar = tqdm(total=N * N)

    # 初始化字典列表
    rectangle_dicts = []
    circle_dicts = []
    ring_dicts = []

    # 迭代计数变量
    n = 1
    # =========遍历每个结构===========
    for i, j in indices:
        if n >= opt.stop_num > 0:
            break
        if (X[i, j] * units) ** 2 + (Y[i, j] * units) ** 2 <= r ** 2:
            structure_type = int(structure[i, j])
            if 10000 <= structure_type < 20000:
                # 绘制square结构，正方形L是边长
                rectangle_dict = {f"rectangle_{n}": layout << gf.components.rectangle(
                    size=(L[i, j] * units, L[i, j] * units), layer=(1, 0))}
                rectangle_dict[f"rectangle_{n}"].move((X[i, j] * units, Y[i, j] * units))
                rectangle_dicts.append(rectangle_dict)
            elif 20000 <= structure_type < 30000:
                # 绘制circle结构,圆中L是半径
                circle_dict = {f"circle_{n}": layout << gf.components.circle(radius=L[i, j] * units,
                                                                             angle_resolution=2.5 * units,
                                                                             layer=(2, 0))}
                circle_dict[f"circle_{n}"].move((X[i, j] * units, Y[i, j] * units))
                circle_dicts.append(circle_dict)
            elif structure_type >= 30000:
                # 绘制ring结构，环L是外径,W是内径
                radius, width = get_radius_width(outer_radius=L[i, j] * units, inner_radius=W[i, j] * units)
                ring_dict = {f"ring_{n}": layout << gf.components.ring(radius=radius,
                                                                       width=width,
                                                                       angle_resolution=2.5 * units,
                                                                       layer=(3, 0))}
                ring_dict[f"ring_{n}"].move((X[i, j] * units, Y[i, j] * units))
                ring_dicts.append(ring_dict)
        # =========判断结束===========
        n += 1
        p_bar.update(1)
        p_bar.set_description(f"i:{i}/{N},j:{j}/{N}")
    # =========循环结束===========
    # p_bar.close()

    # 写入文件
    layout.write_gds(create_filename())

    if opt.show:
        # show it in klayout
        layout.show()
        # plot it in jupyter notebook
        # layout.plot()

    return layout


if __name__ == '__main__':
    from main import parse_args

    draw_structure(parse_args())
