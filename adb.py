import os
from subprocess import check_output


class adb(object):

    @staticmethod
    def devices():
        lines = os.popen("adb devices").readlines()
        return [line.split()[0] for line in lines if len(line.split()) == 2]

    @staticmethod
    def screening(size=('480', '853'), udid=None):
        adbcmd = "adb {0} exec-out screenrecord --bit-rate=16m  --output-format=h264 - | ".format(
            "-s " + udid if udid else "")
        print(adbcmd)
        playcmd = "ffplay -framerate 60 -framedrop -noinfbuf -analyzeduration 40000 -probesize 300000 " \
                  "-x {0} -y {1} -an -window_title \"ACS:{2}\" -".format(size[0], size[1], adb.modelName(udid))
        print(playcmd)
        cmd = adbcmd + playcmd
        print(cmd)
        co = check_output("cmd /c " + cmd, timeout=10)
        print(co)
        # co = os.popen(cmd).readlines
        if "Invalid data found when processing input" in str(co):
            raise Exception("Device not connected")

    @staticmethod
    def modelName(udid=None):
        return os.popen("adb {0} shell getprop ro.product.model".format(" -s " + udid if udid else "")).readline().strip()

    @staticmethod
    def screenSize(udid=None):
        """
        :return: 1080,1920 e.g.
        """
        density = os.popen("adb {0} shell \"dumpsys window | grep mUnrestrictedScreen\"".format(
            " -s " + udid if udid else "")).readline().split()[1]
        return density.split("x")[0], density.split("x")[1]

    @staticmethod
    def ip(udid=None):
        """
        :return: ip address
        """
        return os.popen("adb {0} shell \"ifconfig | grep Mask\"".format(
            " -s " + udid if udid else "")).readline().split()[0].split(":")[-1]

    @staticmethod
    def androidVersion(udid=None):
        return os.popen(
            "adb {0} shell getprop ro.build.version.release".format(" -s " + udid if udid else "")).readline().strip()

    @staticmethod
    def packageActivity(udid=None):
        """
        :return: appPackage, appActivity
        """
        adbcmd = 'adb{0} shell "dumpsys activity|grep {1}"'.format(
            " -s " + udid if udid else "",
            "mResumedActivity" if int(
                adb.androidVersion(udid if udid else None).split(".")[0]) >= 8 else "mFocusedActivity")
        line = os.popen(adbcmd).readline().split()[-2].split("/")
        return line[0], line[1]
