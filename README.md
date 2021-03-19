# Tetris
俄罗斯方块教程，基于python tkinter实现

## 1 基础版
对应文件夹：1_BASIC
本项目基础版最终效果见本人b站投稿[av81480858](https://www.bilibili.com/video/av81480858) 简介部分

本文已录制视频教程上传b站：https://www.bilibili.com/video/av81480858 。视频部分讲解的比较详细，觉得文字版不够详细的可以去看视频。

## 3 AI自动玩俄罗斯方块
对应文件夹：3_AI
运行效果见本人b站投稿[av82337073](https://www.bilibili.com/video/av82337073)

其中multi_tetris.py对应宽屏多个

tetris_by_class.py对应单个竖屏

# 原作者代码基础上练习修改：

1. 在1_BASIC目录中，单独新建文件test.py, test1.py, 通过导入pygame库给游戏增加背景音乐，增加消除，落地，游戏结束的音效
2. 另外扩展游戏面板，在右方区域增加分数显示，下一个方块显示

最后版本为TetrisTk.py 是学习大爽代码，完善音效功能的代码，主要是通过Tkinter模块实现的
另外还有个TetrisPygame.py是另外一个作者的用pygame实现的游戏代码，可以相互参考
