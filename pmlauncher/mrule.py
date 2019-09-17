import platform
import os

checkOSRules = True

is64bit = platform.machine().endswith('64')
osversion = platform.release()
osname = ""
sysname = platform.system()
if sysname == "Linux":
    osname = "linux"
elif sysname == "Darwin":
    osname = "osx"
else:
    osname = "windows"


def checkAllowOS(arr):
    for job in arr:
        action = True  # allow / disallow
        containCurrentOS = True

        for key, value in job.items():
            if key == "action":
                if value == "allow":
                    action = True
                else:
                    action = False
            elif key == "os":
                for osKey, osValue in value.items():
                    if osKey == "name" and osValue == osname:
                        containCurrentOS = True
                        break
                containCurrentOS = False

            elif key == "features":
                return False

        if not action and containCurrentOS:
            return False
        elif action and containCurrentOS:
            return True
        elif action and not containCurrentOS:
            return False


