# Anime-Annotation-Tool

功能模仿 PixelAnnotationTool ，使用 OpenCV 的分水岭算法分割画面

利用OpenCV的稠密光流分析实现了简单的运动跟踪

可以直接加载视频并识别变化较大的帧用于标注（见底部柱形图）

目前功能未完善，暂时的使用方法如下：

1. 安装python环境
2. 安装opencv、flask 、flask_cors
3. 编辑config.json，修改videoPath为视频路径，在configDict以视频文件名为key添加一项，值为label配置文件的路径（内容参考已有的示例）
4. 运行anime.py，复制终端窗口输出的URL到浏览器打开（应为http://127.0.0.1:5000/）。如提示缺少某python包，请安装。

### 试用视频：

https://www.bilibili.com/video/BV1Lf4y1A7tE