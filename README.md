# Robophage  
**似噬菌体的6足机器人**  
***

<div align="center">
  <img src="https://github.com/NowLoadY/Robophage/blob/main/Pictures/%E9%A2%84%E8%A7%88%E5%9B%BE2.png" width="40%" height="40%"/><img src="https://github.com/NowLoadY/Robophage/blob/main/Pictures/%E9%A2%84%E8%A7%88%E5%9B%BE1.png" width="40%" height="40%"/>
</div>  

## 使用的工具/材料  
|       |**Blender**|**Python**|
|:----- |:-----:|:----:|
|简介   |开源免费建模动画软件|解释型编程语言|
|特点|强大的开源社区|简洁性、易读性以及可扩展性|
|用处  |建模、制作动画|处理图像和[监听键盘](https://blog.csdn.net/coco56/article/details/107847467) |
|       |**[RaspberryPi Pico](https://pico.org.cn/)**|**[ESP32cam](https://docs.ai-thinker.com/esp32-cam)**|
|简介    |support programming in C or in micropython|小尺寸摄像头模组 |
|特点|rp2040|Wifi|
|用处  |主控|无线图像传输|
|       |**PCA9685**|**[微型隔膜泵](https://m.tb.cn/h.fEWZDlZ?tk=fhnS2oLF5j6)**|
|简介    |16路舵机控制板iic通信|足够迷你的5v驱动隔膜泵|
|特点|iic|5v工作|
|用处  |控制16个舵机|水操作|
|       |**[转压模块](https://m.tb.cn/h.fvNk34G?tk=g5z52MGwKzn)**|**3s航模锂电池**|
|简介    |in:7V~28V out:5V3A,1.5A if have worked for a long time|about 11.1v|
|特点|5V3A|11.1V|
|用处  |转出工作电压|作为总电源|
|       |**[无线串口模块DL-20](https://item.taobao.com/item.htm?spm=a230r.1.14.24.12c4259eXgpoSP&id=573882263589&ns=1&abbucket=4#detail)**|**FDM3D打印机**|
|简介    |zigbee通信，即插即用|[FDM（Fused deposition Modeling）是熔融沉积成型法的简称，是当前全世界应用最为广泛的3D打印技术](https://zhuanlan.zhihu.com/p/392174214)|
|特点|点对点通信或广播通信|打印步骤较光固化更简单|
|用处  |电脑与单片机的通信|将电脑上建好的模型打印出来|  
***
## 如何  
### 步态（Gait）  
#### 动画  
单腿半圆形轨迹动画以及3角步态动画  

<div align="center">
  <img src="https://github.com/NowLoadY/Robophage/blob/main/Pictures/%E5%8D%95%E8%85%BF%E5%8A%A8.gif" width="40%" height="40%"/><img src="https://github.com/NowLoadY/Robophage/blob/main/Pictures/6%E8%85%BF%E5%8A%A8.gif" width="40%" height="40%"/>
</div>  

#### 细节  
纯纯三角步态  
![步态参考图](https://s2.51cto.com/images/blog/202109/27/7ff3b4724457d457d1847e6c0859d8e2.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=)  
以底盘中心为坐标原点，通过坐标变换和运动学逆解规划足尖实际运动轨迹。  
### 水操作  
#### 吸水和排水  
![物质取放](Pictures/吸水吐水.gif)  
#### 结构  
![模型截图](Pictures/简易水循环系统.png)
### 视觉分类和跟踪  
#### 测试演示（Speed X 3）  
![物质取放](Pictures/图像识别手势控制.gif)  
#### 方法  
从esp32cam获取无线传输的图像，使用预训练的[coco数据集](https://blog.csdn.net/qq_41185868/article/details/82939959)在yolov5上去推理，手势识别使用Google开源机器学习框架[mediapipe](https://mediapipe.dev/)的手部关键点检测。计算分析手势为伸出食指时，将食指的图像投影坐标相对图像中心点的x、y轴偏移量转化为指令发送给机器人调整姿态实现追踪。
***
## Start Building  
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
#### 3d Models  
> StlFiles  
>> body  
>> leg  
>> smallparts  
***
## Video  
现效果请看视频：  
[B站NowLoadY 仿噬菌体的6足机器人](https://www.bilibili.com/video/BV1Ng41197Ls?share_source=copy_web)  
