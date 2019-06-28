import os
from config import msgbx, adb_required, OS


class adb(object):

    @staticmethod
    @adb_required
    def devices():
        lines = os.popen("adb devices").readlines()
        devs = [line.split()[0] for line in lines if len(line.split()) == 2]
        return devs

    @staticmethod
    @msgbx
    def screening(size=("320", "480"), udid=None, noborder=False):
        adbcmd = "adb {0} exec-out \"while true;do screenrecord --bit-rate=16m  --output-format=h264 - ;done\" | ".format(
            "-s " + udid if udid else "")
        playcmd = "ffplay -framerate 60 -framedrop -noinfbuf -analyzeduration 40000 -probesize 300000 " \
                  "-x {0} -y {1} -an {2} -window_title \"ARS: {3}\" -".format(size[0], size[1],
                                                                              "-noborder" if noborder else "",
                                                                              adb.modelName(udid))

        cmd = "cmd /c " + adbcmd + playcmd if OS.startswith("win") else adbcmd + playcmd
        os.popen(cmd)
        # if "Invalid data found when processing input" in co.strip().decode():
        #     messagebox.showerror(title="Error", message="Unexpected parameters or device disconnected")
        #     raise ConnectionAbortedError

    @staticmethod
    @msgbx
    def modelName(udid=None):
        return os.popen(
            "adb {0} shell getprop ro.product.model".format(" -s " + udid if udid else "")).readline().strip()

    @staticmethod
    @msgbx
    def screenSize(udid=None):
        """
        :return: 1080,1920 e.g.
        """
        density = os.popen("adb {0} shell \"dumpsys window | grep mUnrestrictedScreen\"".format(
            " -s " + udid if udid else "")).readline().split()[1]
        return density.split("x")[0], density.split("x")[1]

    @staticmethod
    @msgbx
    def ip(udid=None):
        """
        :return: ip address
        """
        return os.popen("adb {0} shell \"ifconfig | grep Mask\"".format(
            " -s " + udid if udid else "")).readline().split()[0].split(":")[-1]

    @staticmethod
    @msgbx
    def androidVersion(udid=None):
        return os.popen(
            "adb {0} shell getprop ro.build.version.release".format(" -s " + udid if udid else "")).readline().strip()

    @staticmethod
    @msgbx
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
