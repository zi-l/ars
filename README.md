# Ars
[![license](https://img.shields.io/github/license/zi-l/ars.svg?style=for-the-badge)](https://github.com/zi-l/ars/blob/master/LICENSE)
[![release](https://img.shields.io/github/downloads/zi-l/ars/total.svg?color=green&style=for-the-badge)](https://github.com/zi-l/ars/releases)

Ars is a tool screening android devices via [adb](https://developer.android.com/studio/command-line/adb) and [ffplay](https://ffmpeg.org/ffplay.html) (a minimalistic multimedia player of [ffmpeg](https://github.com/FFmpeg/FFmpeg)).


### Requirements
- [adb](https://developer.android.com/studio/command-line/adb)
- [ffplay](https://ffmpeg.org/ffplay.html) (refer to [ffmpeg](https://github.com/FFmpeg/FFmpeg))

### Manual

#### Installation
Download release file `xxx.zip`, extract to anywhere, and then run `ars.exe`

#### Usage
There's three buttons on the widget.

- `Start` button on the right side. Click to detect connected devices or start screening once some of devices selected.
- `Stop` button in the middle. Click to stop all screening.
- `Kill` button on the left side. Click to kill adb and ffplay processes.

[![ars](https://github.com/zi-l/ars/blob/master/docs/image/ars.png)](https://github.com/zi-l/ars/blob/master/docs/image/ars.png)

[![select](https://github.com/zi-l/ars/blob/master/docs/image/select.png)](https://github.com/zi-l/ars/blob/master/docs/image/select.png)

[![screening](https://github.com/zi-l/ars/blob/master/docs/image/screening.png)](https://github.com/zi-l/ars/blob/master/docs/image/screening.png)


### Limitation
- Ars only support screening via USB connection. WIFI screening is not being implemented so far.
- Ars only screening android device, it's not possible to control android device through screening.
