"""
# -*- coding:utf-8 -*-
# @Project    : DrawMetalensStructure
# @FileName   : circle.py
# @Author     : Spring
# @Time       : 16/04/2024 18:01
# @Description: 
"""
import numpy as np
import pya
from klayout.pyacore import DPolygon, DPoint


def circle(
        radius: float = 10.0,
        angle_resolution: float = 2.5,
        # layer: LayerSpec = "WG",
):
    """Generate a circle geometry.

    Args:
        radius: of the circle.
        angle_resolution: number of degrees per point.
        layer: layer.
    """
    if radius <= 0:
        raise ValueError(f"radius={radius} must be > 0")
    t = np.linspace(0, 2 * np.pi, int(2 * np.pi / np.radians(angle_resolution)))
    print(len(t))
    xpts = (radius * np.cos(t)).tolist()
    print(xpts)
    ypts = (radius * np.sin(t)).tolist()
    # pya.DPolygon
    points = [DPoint(xpts[i], ypts[i]) for i in range(len(t))]
    print(points)
    return DPolygon(points)


if __name__ == "__main__":
    layout = pya.Layout()
    layout.dbu = 100  # 1nm
    top = layout.create_cell("TOP")
    l1 = layout.layer(1, 0)
    circle1 = circle(10, 0.5)
    top.shapes(l1).insert(circle1)

    layout.write("t.gds")
