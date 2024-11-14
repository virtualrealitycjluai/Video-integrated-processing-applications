# 基于深度学习的视频处理软件

    本软件集成了视频的降噪，超分，插帧等功能。

## 硬件及平台要求 
 NVIDIA系列显卡（支持CUDA，4GB显存及以上）
 windows 10及以上

## 1 安装
### 1.1 安装[anaconda](https://www.anaconda.com/download/success)
此项目基于不同的深度学习方法实现，包管理器是必要的。[什么是anaconda？](https://www.zhihu.com/tardis/zm/art/96990748)
### 1.2 新建一个虚拟环境
找到anaconda安装目录，点击地址栏，键入cmd
![图片说明](example.png)  
在打开的命令行窗口中依次执行下述语句

    cd Anaconda3/condabin
    conda activate
    conda create -n env_1 python == 3.7.6
### 1.3 进入虚拟环境
    conda activate env_1
### 1.4 安装插帧功能所需的python软件包
* pytorch==1.5.1 torchvision==0.6.1
* cudatoolkit==10.1
* cupy==7.5.0
* pillow==8.2.0
* einops==0.3.0
  
  [如何安装python软件包？](https://blog.csdn.net/qq_42692386/article/details/113881379)
    
### 1.5 安装降噪功能所需要的python软件包

重复1.2和1.3的操作再次新建一个虚拟环境
* opencv-python
* scikit-image
* pillow
* torchvision
* hdf5storage
* ninja
* lmdb
* requests
* timm
* einops

### 1.6 安装超分功能所需要的python软件包

重复1.2和1.3的操作再次新建一个虚拟环境
* basicsr>=1.4.2
* facexlib>=0.2.5
* gfpgan>=1.3.5
* numpy
* opencv-python
* Pillow
* torch>=1.7
* torchvision
* tqdm
## 降噪

## 超分

## 插帧

该功能基于[Video Frame Interpolation Transformer](https://github.com/zhshi0816/Video-Frame-Interpolation-Transformer?tab=readme-ov-file)项目实现

使用数据集[Vimeo-90K septuplets](http://toflow.csail.mit.edu/)

更多可供评估的数据集：
* [UCF](https://www.google.com/url?q=https%3A%2F%2Fwww.dropbox.com%2Fs%2Fdbihqk5deobn0f7%2Fucf101_extracted.zip%3Fdl%3D0&sa=D&sntz=1&usg=AFQjCNE8CyLdENKhJf2eyFUWu6G2D1iJUQ)
* [Davis](https://www.google.com/url?q=https%3A%2F%2Fwww.dropbox.com%2Fs%2F9t6x7fi9ui0x6bt%2Fdavis-90.zip%3Fdl%3D0&sa=D&sntz=1&usg=AFQjCNG7jT-Up65GD33d1tUftjPYNdQxkg)
