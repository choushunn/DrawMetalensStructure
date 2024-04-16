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

from utils import create_filename, read_data, get_radius_width


def draw_structure(opt):
    """
    绘制结构
    :param opt:输入参数
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
    # 初始化字典,必须定义字典
    rectangle_dict = {}
    circle_dict = {}
    ring_dict = {}
    # 迭代计数变量
    n = 1
    if opt.show:
        # 显示进度条
        p_bar = tqdm(total=opt.stop_num if opt.stop_num > 0 else N * N)
    # =========遍历每个结构===========
    for i, j in indices:
        if n >= opt.stop_num > 0:
            break
        if (X[i, j] * units) ** 2 + (Y[i, j] * units) ** 2 <= r ** 2:
            structure_type = int(structure[i, j])
            if 10000 <= structure_type < 20000:
                # 绘制square结构，正方形L是边长
                rectangle_dict[f"rectangle_{n}"] = layout << gf.components.rectangle(
                    size=(L[i, j] * units, L[i, j] * units), layer=(1, 0))
                rectangle_dict[f"rectangle_{n}"].move((X[i, j] * units, Y[i, j] * units))
            elif 20000 <= structure_type < 30000:
                # 绘制circle结构,圆中L是半径
                circle_dict[f"circle_{n}"] = layout << gf.components.circle(radius=L[i, j] * units,
                                                                            angle_resolution=0.5,
                                                                            layer=(2, 0))
                circle_dict[f"circle_{n}"].move((X[i, j] * units, Y[i, j] * units))
            elif structure_type >= 30000:
                # 绘制ring结构，环L是外径,W是内径
                radius, width = get_radius_width(outer_radius=L[i, j] * units, inner_radius=W[i, j] * units)
                ring_dict[f"ring_{n}"] = layout << gf.components.ring(radius=radius,
                                                                      width=width,
                                                                      angle_resolution=0.5,
                                                                      layer=(3, 0))
                ring_dict[f"ring_{n}"].move((X[i, j] * units, Y[i, j] * units))
        # =========判断结束===========
        n += 1
        if opt.show:
            p_bar.update(1)
            p_bar.set_description(f"i:{i}/{N},j:{j}/{N}")
    # =========循环结束===========
    # p_bar.close()
    # 写入文件
    layout.write_gds(create_filename())

    # if opt.show:
    # show it in klayout
    # layout.show()
    # plot it in jupyter notebook
    # layout.plot()
    return layout


def draw_demo():
    """
    示例代码
    :return:
    """
    # 定义画布
    layout = gf.Component("Demo")
    # 画矩形
    rectangle = gf.components.rectangle(size=(10, 20), layer=(1, 0))
    # 添加到画布，旋转45度，移动到(-10,-10)
    layout.add_ref(rectangle).rotate(45).move((-10, -10))
    # 画圆
    circle = gf.components.circle(radius=5, angle_resolution=2.5, layer=(2, 0))
    # 添加到画布，移动到(0,16)
    layout.add_ref(circle).move((0, 16))
    # 画三角形
    triangle = gf.components.triangle(x=10, y=14, layer=(4, 0))
    # 添加到画布，移动到(55,35)
    layout.add_ref(triangle).move((55, 0))
    # 画直线
    line = gf.components.straight(length=10, layer=(5, 0))
    # 添加到画布，移动到(55,35)
    layout.add_ref(line).move((55, 35))
    # 画圆环
    radius, width = get_radius_width(10, 6)
    ring = gf.components.ring(radius=radius, width=width, angle_resolution=2.5, layer=(3, 0))
    layout.add_ref(ring).move((0, 16))
    # 写入文件
    layout.write_gds(f"output/demo.gds")
    # layout.show()


def read_append_demo(opt):
    """
    读取现有画布，并追加
    :param opt: 输入参数
    :return:
    """
    # 读取现有画布
    layout_a = gf.read.import_gds("output/test-4metalens20240414.gds", cellname="top")
    # 新建画布
    layout = gf.Component("Demo2")
    # 在新画布中画矩形
    rectangle1 = gf.components.rectangle(size=(15 * 1e-3, 5 * 1e-3), layer=(2, 0))
    layout.add_ref(rectangle1).rotate(60)

    # 将原有的画布追加到新的画布上
    layout.add_ref(layout_a)
    # 写入文件
    layout.write_gds(f"output/layout_a.gds")


if __name__ == '__main__':
    pass
