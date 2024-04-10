# Draw Metalens Structure

## Getting Started

### Python 库

- [klayout](https://www.klayout.org/klayout-pypi/)

```
pip install klayout --upgrade
```

- [gdsfactory](https://gdsfactory.github.io/gdsfactory/developer.html)

```
pip install "gdsfactory[full]" --upgrade
```

### KLayout 及插件

- [KLayout](https://www.klayout.de/build.html#downloads)
- [KLive](https://gdsfactory.github.io/klive/)

## Usage
```shell
# 指定数据文件,开始运行
python main.py --data_file data.mat
               --units 1e-3        
```