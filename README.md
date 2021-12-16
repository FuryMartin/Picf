# Picf

## 简介
Picf 是一款智能相册，由北航2020级电子信息工程学院的学生为完成计算机软件基础大作业而构建。

Picf 主要具有三大功能，均为老师所要求的功能：
- 人脸识别分类：把相册中的图片按人分类。
- 人脸搜索：把同一个人的图片全部筛选出来。
- 重复筛查：把相同的图片筛选出来，剔除重复的文件。

除了这些功能以外，Picf 具有一些额外特性：
- #### **支持手动修改分类结果**
    因图片质量、模型性能等原因，难免会出现将图片分错的情况，Picf 支持用户手动修改图片的分类结果，并将分类结果存储起来。
- #### **支持稳定的渐进式识别**
    在对图片进行识别分类的过程中，Picf 可以根据已分类的结果，将文件夹内新添加的图片合并到已有的人物下面。
- #### **支持相似图片筛查**
    借助 `PHash` 与 `Hamming Distance` 的方法，Picf 可以将相似的图片筛选出来，并由用户决定删除哪些图片。
- #### **美观的图形化界面**
    借助于开源项目，Picf 拥有相对美观、现代的GUI界面，使得分类、搜索、筛查的结果呈现更加直观。
## 安装步骤:
- ### 安装 Anaconda（如果已有，跳过本步）
- ### 下载最新的 Release
- ### 运行`setup.bat`。
    `setup.bat` 主要用于自动创建 conda 环境、安装依赖包、完成`imagededup`包的编译。
## 使用方法：
```
conda activate Picf
python main.py
```
## 原理

### 一、 人脸识别分类
输入一组图片，对于其中的每张图片进行以下步骤：

- 人脸检测：找到图片中的人脸位置，以返回人脸的矩形坐标。
- 人脸对齐：将矩形内部的人脸进行水平、竖直对齐。
- 特征值提取：将对齐的人脸输入 `facenet` 网络，得到该人脸的128维特征向量。

所有图片处理完毕后，对提取到的多张人脸的特征值，使用聚类算法 `Chinese Whispers` 进行聚类，得到分类好的人脸组，并将提取到的特征值和分类结果保存。

### 二、 人脸搜索
输入一张图片，依次进行以下步骤：

- 按照人脸识别分类的方法对图片中的人脸提取特征值。
- 将特征值与已有图片组的特征值一起使用 `Chinese Whispers` 算法聚类。
- 根据已保存的分类结果，将输入图片中人物的所有图片输出。

### 三、 相似图片筛查
输入一组图片，依次进行以下步骤：

- 获取每张图片的 `PHash` 值。
- 计算图片间的 `Hamming distance` 。
- 使用 `BKTree` 按 `Hamming distance` 的大小对照片进行分组，输出分组结果。

## 致谢
在构建Picf的过程中，我们参考并使用了以下开源仓库的代码：

- ### [yashyenugu/Sort-By-Face](https://github.com/yashyenugu/Sort-By-Face)
    提供了人脸识别、分类的基本框架。
- ### [Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
    提供了高效、准确、轻量的人脸检测器。
- ### [idealo/imagededup](https://github.com/idealo/imagededup)
    提供了相似图片筛查的方案。
- ### [Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI](https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI)
    提供了GUI框架，对于完全没有GUI开发经验的我们而言，非常有帮助。
