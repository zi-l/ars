import os
import subprocess
from subprocess import check_output, call
from datetime import datetime

from serv import serv

FFPLAY = "ffplay.exe"
ADB = "adb.exe"


class adb(object):

    @staticmethod
    def devices():
        lines = os.popen("adb devices").readlines()
        return [line.split()[0] for line in lines if len(line.split()) == 2]

    @staticmethod
    def screening(size=('480', '853'), udid=None):
        adbcmd = "adb {0} exec-out \"while true;do screenrecord --bit-rate=16m  --output-format=h264 - ;done\" | ".format(
            "-s " + udid if udid else "")
        playcmd = "ffplay -framerate 60 -framedrop -noinfbuf -analyzeduration 40000 -probesize 300000 " \
                  "-x {0} -y {1} -an -window_title \"ARS: {2}\" -".format(size[0], size[1], adb.modelName(udid))
        cmd = adbcmd + playcmd
        # print(cmd)
        # ti = datetime.now()
        # co = check_output("cmd /c " + cmd, timeout=30)
        call("cmd /c " + cmd)
        # co = subprocess.Popen("cmd /c " + cmd, stderr=subprocess.PIPE)
        # co = co.stderr.readlines()[-1].strip().decode()
        # print(co.strip().decode())
        # print((datetime.now()-ti).seconds)
        # if "Invalid data found when processing input" in co.strip().decode():
        #     raise Exception("Device not connected or parameters invalid")
        # while serv.alive(FFPLAY):
        #     # print('in')
        #     continue

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