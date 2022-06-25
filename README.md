# Robophage  
**仿噬菌体的6足机器人**  
***
![图片](resource/RobophageBlender.png)  
## Start Building  
> 持续优化改进...  
### code  
#### RaspberryPi Pico  
  把resource/code/pico内，main.py所在的路径作为根路径，烧写在RaspberryPi Pico上，上电自动运行。  
settings.py是设置文件  
**main.py**中的循环前的语句有配置详情，根据这些代码可以知道如何接线。  
#### Personal Computer  
  resource/code/Controller，内含yolo，所以带了一份yolo6.1的requirements.txt  
  运行**user.py**
***
### Parts of the machine  
#### 身体  
使用blender建模，身体中间有一条竖直的管道，用于存储、传输物质或又可加装拓展设备，例如激光、燃气焊枪、机械爪、伸缩式探头、马克笔，甚至是螺旋桨、火箭推进器等。  
头部也有足够的空间（相对的比例来说），可安装高性能计算单元。  
#### 腿部  
使用开源项目“[hexapod，这里给一个python版传送门](https://github.com/ViolinLee/PiHexa18)”的腿，正六边形插入式安装。
关节动力目前采用舵机，up正在学习无刷电机。  
#### 3d模型整理后上传  
***
## 效果视频  
目前有如下的效果：  
[B站NowLoadY 仿噬菌体的6足机器人](https://www.bilibili.com/video/BV1Ng41197Ls?share_source=copy_web)  
