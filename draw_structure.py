"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : draw_structure.py
# @Author     : Spring
# @Time       : 10/04/2024 17:30
# @Description: 
"""
import numpy as np

from tqdm import tqdm
import gdsfactory as gf

from utils import create_filename, read_data


def draw_structure(data_file, nm=1e-3, show=False):
    """
    绘制结构
    :param show: 是否显示
    :param nm:
    :param data_file:数据文件名
    :return:
    """
    data = read_data(data_file)
    # 获取数据
    X, Y, L, W, structure = data['X'], data['Y'], data['L'], data['W'], data['structure']
    # 创建画布
    layout = gf.Component("My_Layout")
    # 计算总结构数
    N = len(X)
    # 计算索引
    indices = np.indices((N, N)).reshape(2, -1).T
    # 计算半径
    r = (np.sqrt(1.8 ** 2 + 1.8 ** 2) + 1.6) * 10 ** 7
    # 初始化字典,必须定义字典
    rectangle_dict = {}
    circle_dict = {}
    ring_dict = {}
    # 迭代计数变量
    n = 1
    # 初始化进度条
    p_bar = tqdm(total=N * N)
    # =========遍历每个结构===========
    for i, j in indices:
        if (X[i, j] * nm) ** 2 + (Y[i, j] * nm) ** 2 <= r ** 2:
            structure_type = int(structure[i, j])
            if 10000 <= structure_type < 30000:
                if 10000 <= structure_type < 20000:
                    # 绘制square结构，正方形L是边长
                    rectangle_dict[f"rectangle_{n}"] = layout << gf.components.rectangle(
                        size=(L[i, j] * nm, L[i, j] * nm), layer=(1, 0))
                    rectangle_dict[f"rectangle_{n}"].move((X[i, j] * nm, Y[i, j] * nm))
                elif 20000 <= structure_type < 30000:
                    # 绘制circle结构,圆中L是半径
                    circle_dict[f"circle_{n}"] = layout << gf.components.circle(radius=L[i, j] * nm,
                                                                                angle_resolution=2.5 * nm, layer=(2, 0))
                    circle_dict[f"circle_{n}"].move((X[i, j] * nm, Y[i, j] * nm))
                elif structure_type >= 30000:
                    # 绘制ring结构，环L是外经W是内径
                    ring_dict[f"ring_{n}"] = layout << gf.components.ring(radius=L[i, j] * nm,
                                                                          width=L[i, j] * nm - W[i, j] * nm,
                                                                          angle_resolution=2.5 * nm,
                                                                          layer=(3, 0))
                    ring_dict[f"ring_{n}"].move((X[i, j] * nm, Y[i, j] * nm))
        # =========判断结束===========
        n += 1
        p_bar.update(1)
        p_bar.set_description(f"i:{i}/{N},j:{j}/{N}")
    # =========循环结束===========
    p_bar.close()
    # plot it in jupyter notebook
    # layout.plot()
    # 写入文件
    layout.write_gds(create_filename())
    if show:
        # show it in klayout
        layout.show()

    return layout
