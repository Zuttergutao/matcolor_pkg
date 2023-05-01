# MATCOLOR

## 前言

`matcolor`是一个能够提供matplotlib绘图colormap以及从图片中识别特征颜色的python包。目前支持R包[MetBrewer](https://github.com/BlakeRMills/MetBrewer)从世界名画中提取的颜色方案（它也提供了python包），同时我添加了一个从图片中提取色彩的小功能，该功能提取色彩的方法较为简单且粗糙，但是够用。

强烈建议`matcolor`结合`jupyter notebook`一起使用，这样可以更加直观的获得颜色数据。

> 此项目受到`阿昆的科研日常`开发的matlab插件`TC`以及R包[MetBrewer](https://github.com/BlakeRMills/MetBrewer)的启发得来。  
>
> 因为水平有限，代码的逻辑结构和编写上会出现一些问题，欢迎提供意见！

## 安装

目前该插件还处于开发中，仅提供安装包安装

1. 从[github仓库](https://github.com/Zuttergutao/matcolor_pkg)上下载文件夹

2. 解压文件夹并在文件夹下运行如下命令（注意当前的python版本）：

    ```python
    python setup.py install 
    ```

## 使用

### 生成离散色

直接使用包内提供的颜色名进行绘图

```python
import matplotlib.pyplot as plt
import matcolor

x = ["a", "b", "c", "d", "e", "f"]
y = [1.2, 0.8, 2.5, 0.95, 1.35, 1.58]
fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(x, y, color=matcolor.matcolor().dcolor("Archambault"))
```

<img src="test\IMG\3.png" alt="1" style="zoom:50%;" />

同时也支持从图片中提取颜色绘图，只需要设置图片路径以及提取颜色数目即可

```python
import matplotlib.pyplot as plt
import matcolor

x = ["a", "b", "c", "d", "e", "f"]
y = [1.2, 0.8, 2.5, 0.95, 1.35, 1.58]
fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(x, y, color=matcolor.matcolor().dcolor(useimg=True,imgpath="IMG/coin.png",numcolors=6))
```

<img src="test\IMG\4.png" alt="1" style="zoom:50%;" />

### 内置colormap

内置colormap提取自R包[MetBrewer](https://github.com/BlakeRMills/MetBrewer)，用户可以使用如下命令获取提供的全部色彩图以及相应名称

```python
import matcolor
matcolor.matcolor().draw_cm()
```

<img src="test\IMG\1.png" alt="1" style="zoom:50%;" />

也可以通过指定colormap名打印指定colormap：

```python
import matcolor
matcolor.matcolor().draw_cm(show="Archambault")
```

<img src="test\IMG\2.png" alt="1" style="zoom:50%;" />

### 添加colormap

此方法能够将colormap写入到dcolor.xml文件中，后续使用时可以根据命名调用。

```python
import matcolor

cmap=['#88a0dc','#381a61','#7c4b73','#ed968c','#ab3329','#e78429','#f9d14a']
matcolor.matcolor().add_colormap("test",cmap=cmap)
matcolor.matcolor().draw_cm(show="test")
```

### 删除colormap

```python
import matcolor

matcolor.matcolor().del_colormap("test")
```

### 获取颜色组名和组成

`cmn`为colormap命名，`cm`为对应的颜色组成，顺序是一一对应的

```python
import matcolor

matcolor.matcolor().cm
matcolor.matcolor().cmn
```

### 从图片中提取颜色

指定提取图片，提取颜色数目即可,返回的是颜色数组

```python
import matcolor

matcolor.extract_feature_colors(img_path="IMG/bingbing.png",num_colors=10).colormap()
```

输出颜色图片

```python
import matcolor

matcolor.extract_feature_colors(img_path="IMG/bingbing.png",num_colors=10).draw_cm(savefig=True)
```



## 小结与Todo

第一次写python package，python学的还是太浅了，这个项目搭起来也耗了很长时间，但是乐在其中。

目前`matcolor`还处于幼儿时期，也不知道会不会再更新。如果更新的话应该会从下面几点开始：

> - 提取颜色有很多方法例如PCA，二值化等等，考虑加这些加入进来
> - 优化流程，目前包内色彩都是保存在`dcolor.yaml`中，考虑加入更多的颜色
> - 添加与完善单色和渐变色功能
> - 添加随机选色功能
> - 最后希望打包发布吧！

