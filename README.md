# Ars
Ars is a tool screening android devices via [adb](https://developer.android.com/studio/command-line/adb) and [ffplay](https://ffmpeg.org/ffplay.html) (a minimalistic multimedia player of [ffmpeg](https://github.com/FFmpeg/FFmpeg)).

## Requirements.
- [adb](https://developer.android.com/studio/command-line/adb)
- [ffplay](https://ffmpeg.org/ffplay.html) (refer to [ffmpeg](https://github.com/FFmpeg/FFmpeg))

## Manual
There's three buttons on the widget.

- `Start` button on the right side. Click to detect connected devices or start screening once some of devices selected.
- `Stop` button in the middle. Click to stop all screening.
- `Kill` button on the left side. Click to kill adb and ffplay processes.

[![ars](https://github.com/zi-l/ars/blob/master/docs/image/ars.png)](https://github.com/zi-l/ars/blob/master/docs/image/ars.png)

[![select](https://github.com/zi-l/ars/blob/master/docs/image/select.png)](https://github.com/zi-l/ars/blob/master/docs/image/select.png)

## Limitation
- Ars Only support screening via USB connection. WIFI screening is not implemented so far.
- Ars only screening android device, it's not possible to control android device through screening.
