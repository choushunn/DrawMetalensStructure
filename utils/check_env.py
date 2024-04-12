"""
# -*- coding:utf-8 -*-
# @Project    : main.py
# @FileName   : check_env.py
# @Author     : Spring
# @Time       : 12/04/2024 13:08
# @Description: 
"""

import subprocess


def check_python_version():
    # 获取当前的python版本
    python_version = subprocess.check_output(["python", "--version"], text=True)
    print(f"{python_version}")


def check_requirements():
    """
    检查依赖是否存在
    :return:
    """
    check_python_version()
    packages = [
        {"name": "klayout", "command": "pip install klayout --upgrade"},
        {"name": "gdsfactory", "command": 'pip install "gdsfactory" --upgrade'},
        {"name": "scipy", "command": 'pip install "scipy" --upgrade'},
        {"name": "numpy", "command": 'pip install "numpy" --upgrade'},
        {"name": "tqdm", "command": 'pip install "numpy" --upgrade'},
        # {"name": "tensorboardX", "command": "pip install tensorboardX --upgrade"},
    ]

    print("正在检查环境依赖...")
    for package in packages:
        try:
            # 尝试导入包，如果导入成功则已安装
            __import__(package["name"])
            # print(f"{package['name']} 已安装")
        except ImportError:
            print(f"{package['name']} 未安装，正在尝试安装......")
            # 执行安装命令
            try:
                subprocess.check_call(package["command"], shell=True)
                print(f"{package['name']} 安装成功")
            except subprocess.CalledProcessError:
                print(f"{package['name']} 安装失败")


if __name__ == '__main__':
    check_requirements()
    # check_python_version()
