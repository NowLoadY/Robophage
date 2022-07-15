# Robophage  
**仿噬菌体的6足机器人**  
***
![预览图片](Pictures/预览图2.png)![预览图片](Pictures/预览图1.png)    
***
## How to say: Imitate the phage？  
### 大致外形  
![来自国外论文的图片](Pictures/bacteriophage2.jpg)   
如图，噬菌体的结构最明显的是头部，“Helical sheath”，Hexagonal baseplate，Tail fibers...Tail pins也是很重要的部分。  
### 生理功能
我们都知道噬菌体是一种病毒，最常见的即以大肠杆菌为寄主的T2噬菌体。[当噬菌体T2感染大肠杆菌时，它的尾部吸附在菌体上。然后，菌体内形成大量噬菌体，菌体裂解后，释放出几十个乃至几百个与原来感染细菌一样的噬菌体T2。](http://zhidao.baidu.com/question/370795825/answer/3064369381)  
![网友回答的配图](https://iknow-pic.cdn.bcebos.com/c8177f3e6709c93d6c95af16913df8dcd00054ef)  
这样的机器人怎么能侵入什么东西来实现自己的复制？所以模仿“注入DNA”更合适。  
***
## 使用的Tools/Materials  
|       |**Blender**|**Python**|
|:----- |:-----:|:----:|
|简介   |开源免费建模动画软件|解释型编程语言|
|特点|强大的开源社区|简洁性、易读性以及可扩展性|
|用处  |建模、制作anime|Processing images and [监听键盘](https://blog.csdn.net/coco56/article/details/107847467) |
|       |**[RaspberryPi Pico](https://pico.org.cn/)**|**[ESP32cam](https://docs.ai-thinker.com/esp32-cam)**|
|简介    |support programming in C or in micropython|小尺寸摄像头模组 |
|特点|rp2040|Wifi|
|用处  |main computing chip|Wireless Images Transmission|
|       |**PCA9685**|**[微型隔膜泵](https://m.tb.cn/h.fEWZDlZ?tk=fhnS2oLF5j6)**|
|简介    |16路舵机控制板iic通信|足够迷你的5v驱动隔膜泵|
|特点|iic|5v工作|
|用处  |control 16 servos|water operation|
|       |**[转压模块](https://m.tb.cn/h.fvNk34G?tk=g5z52MGwKzn)**|**3s航模锂电池**|
|简介    |in:7V~28V out:5V3A,1.5A if have worked for a long time|about 11.1v|
|特点|5V3A|11.1V|
|用处  |转出工作电压|作为总电源|
|       |**[无线串口模块DL-20](https://item.taobao.com/item.htm?spm=a230r.1.14.24.12c4259eXgpoSP&id=573882263589&ns=1&abbucket=4#detail)**|**FDM3D打印机**|
|简介    |zigbee通信，即插即用|[FDM（Fused deposition Modeling）是熔融沉积成型法的简称，是当前全世界应用最为广泛的3D打印技术](https://zhuanlan.zhihu.com/p/392174214)|
|特点|点对点通信或广播通信|打印步骤较光固化更简单|
|用处  |电脑与单片机的通信|将电脑上建好的模型打印出来|  
***
## 实现原理  
### 步态  
#### 步态动画  
单腿半圆形轨迹动画  
![单腿](Pictures/单腿动.gif)  
3角步态动画  
![六条腿](Pictures/6腿动.gif)  
#### 步态说明  
纯纯三角步态  
![步态参考图](https://s2.51cto.com/images/blog/202109/27/7ff3b4724457d457d1847e6c0859d8e2.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=)
### 水操作  
#### 取水注水  
![物质取放](Pictures/吸水吐水.gif)  
#### 结构说明  
![模型截图](Pictures/简易水循环系统.png)
### 视觉识别追踪  
#### 测试动图（Speed X 3）  
![物质取放](Pictures/图像识别手势控制.gif)  
#### 方法  
物体识别直接使用yolov5训练的开源[coco数据集](https://blog.csdn.net/qq_41185868/article/details/82939959)模型，手势识别使用Google开源机器学习框架[mediapipe](https://mediapipe.dev/)的手部关键点检测。计算分析手势为伸出食指时，将食指的图像投影坐标相对图像中心点的x、y轴偏移量转化为指令发送给机器人调整姿态实现追踪。esp32cam带来了主要延迟。  
***
## Start Your Building  
### Code  
#### RaspberryPi Pico  
  把resource/code/pico作根路径，烧写在RaspberryPi Pico上。  
**main.py**有配置详情  
#### Personal Computer  
  resource/code/Controller
  运行**user.py**
***
### Parts of the machine  
#### Body  
使用blender建模。  
#### Leg  
使用开源项目“[hexapod，这里给一个python版传送门](https://github.com/ViolinLee/PiHexa18)”的腿，正六边形插入式安装。  
#### 3d模型  
> StlFiles  
>> body  
>> leg  
>> smallparts  
***
## 效果视频  
现有如下效果：  
[B站NowLoadY 仿噬菌体的6足机器人](https://www.bilibili.com/video/BV1Ng41197Ls?share_source=copy_web)  
