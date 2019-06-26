import os
import sys
# import subprocess
# from subprocess import check_output, call
from tkinter import messagebox

from config import msgbx, adb_required


class adb(object):

    @staticmethod
    @adb_required
    def devices():
        lines = os.popen("adb devices").readlines()
        devs = [line.split()[0] for line in lines if len(line.split()) == 2]
        if not devs:
            messagebox.showerror(title="Error", message="No device connected or authorized")
            raise ConnectionError
        return devs

    @staticmethod
    @msgbx
    def screening(size=("320", "480"), udid=None, noborder=False):
        # print('udid: ', udid)
        adbcmd = "adb {0} exec-out \"while true;do screenrecord --bit-rate=16m  --output-format=h264 - ;done\" | ".format(
            "-s " + udid if udid else "")
        playcmd = "ffplay -framerate 60 -framedrop -noinfbuf -analyzeduration 40000 -probesize 300000 " \
                  "-x {0} -y {1} -an {2} -window_title \"ARS: {3}\" -".format(size[0], size[1],
                                                                              "-noborder" if noborder else "",
                                                                              adb.modelName(udid))

        cmd = "cmd /c " + adbcmd + playcmd if sys.platform.startswith("win32") else adbcmd + playcmd
        # print(cmd)
        # call(cmd)
        os.popen(cmd)
        # check_output(cmd)
        # subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # co = check_output("cmd /c " + cmd)
        # print(co.strip().decode())
        # if "Invalid data found when processing input" in co.strip().decode():
        #     messagebox.showerror(title="Error", message="Unexpected parameters or device disconnected")
        #     raise ConnectionAbortedError

    @staticmethod
    def modelName(udid=None):
        return os.popen(
            "adb {0} shell getprop ro.product.model".format(" -s " + udid if udid else "")).readline().strip()

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
        pkat = os.popen(adbcmd).readline().split()[-2].split("/")
        return pkat[0], pkat[1]

    @staticmethod
    def nameUdid():
        devices = {}
        try:
            for ud in adb.devices():
                devices[adb.modelName(ud)] = ud
            return devices
        except:
            return devices
