# TCS

openTCS是开源的调度系统，使用Gradle架构，开源代码实现了基础的功能调度：

* 路由(Route)
* 派遣(Dispacher)
* 调度(schedule)

# 开发内容

根据openTCS的[开发者官方文档](https://www.opentcs.org/docs/4.20/developer/developers-guide/opentcs-developers-guide.html)和[博客开发教程](https://www.cnblogs.com/zjwno1/tag/openTCS/)进行开发，主要实现了：

* 新的通信驱动(driver adapter)
* socket通信工具

能够在车辆执行kernel派遣的订单任务时，通过socket发送任务指令给机器人，并在接受任务完成指令时，更新车辆状态和位置

## 通信机制：

TCS调度车辆并向实体车辆发送socket指令的大体流程如下：

1. 建立连接
2. 发送指令
3. 接受完成指令
4. 断开连接

## 调度算法：

没有修改过kernel内的调度算法，疑似采用向前判断两格有没有车的机制，但不锁定，容易造成死锁等安全问题，两种解决方法：

1. 修改调度算法
2. 在建图、规划地图时，路口附近额外加入缓冲点，并尽量避免双向路段的规划

# 如何开发和运行

## 环境

1. Gradle
2. jdk
3. IDEA

## 项目文件

开发和运行主体主要分为三个部分：

1. Kernel
2. KernelControlCenter
3. PlantOverview

## 运行方式：
运行顺序：Kernel必须在KernelControlCenter之前运行，PlantOverview无所谓

运行方法主要分两种：
* 直接编译运行：
    IDEA中依次运行上述三个Gradle项目中的   `Tasks` -> `application` -> `run`
* 运行编译后的.sh文件
    .sh文件位于(以kernel为例)： `~/openTCS-Kernel/build/install/openTCS-Kernel/startKernel.sh`
  
操作流程：

1. 编辑地图或加载地图 `File` -> `Load Model`
2. 持久化地图到内核中（加载地图） `File` -> `Persist Model in the kernel`
3. 切换至操作模式 `File` -> `Mode` -> `Operating Mode`
4. 在车辆控制中心开启车辆 `Kernel Control Center` -> `Vehicle Driver` -> `Enabled`
5. 修改车辆接受信息类型 `Plant Overview` -> `Vehicles` -> 车辆右键 -> `Change integration level` -> `to utilize this vehicle for transport orders`
6. 添加运输订单 `Action` -> `Create transport order`
