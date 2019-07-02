# Ars
[![license](https://img.shields.io/github/license/zi-l/ars.svg?style=for-the-badge)](https://github.com/zi-l/ars/blob/master/LICENSE)
[![release](https://img.shields.io/github/downloads/zi-l/ars/total.svg?color=green&style=for-the-badge)](https://github.com/zi-l/ars/releases)

- [English](https://github.com/zi-l/ars/blob/master/README.md)

Ars是一个通过[adb](https://developer.android.com/studio/command-line/adb)和[ffplay](https://ffmpeg.org/ffplay.html) （一个[ffmpeg](https://github.com/FFmpeg/FFmpeg)的极简多媒体播放器子工具）对安卓设备进行投屏的工具.


### 依赖
- [adb](https://developer.android.com/studio/command-line/adb)
- [ffplay](https://ffmpeg.org/ffplay.html) （参考[ffmpeg](https://github.com/FFmpeg/FFmpeg)）

### 用户指南

#### 安装
下载最新版本 `xxx.zip`, 解压到任意位置, 运行可执行文件`ars.exe`

#### 使用
主界面有三个按钮

- `Start` 按钮位于右侧。点击以检测连接的设备或者对选择的设备开始进行投屏。
- `Stop` 按钮位于中间。点击关闭所有投屏，但保留adb进程。
- `Kill` 按钮位于最左侧。点击杀死所有adb和ffplay进程。

*初始界面*
[![ars](https://github.com/zi-l/ars/blob/master/docs/image/ars.png)](https://github.com/zi-l/ars/blob/master/docs/image/ars.png)

*选择设备进行投屏*
[![select](https://github.com/zi-l/ars/blob/master/docs/image/select.png)](https://github.com/zi-l/ars/blob/master/docs/image/select.png)


### 局限
- Ars目前仅支持通过USB连接进行投屏，WIFI连接尚不支持。
- Ars仅仅是对安卓屏幕进行投影，无法通过投屏操控安卓设备。
