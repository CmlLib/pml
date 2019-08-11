import platform
from pmlauncher import minecraft
import os

class mlibrary:
    def __init__(self):
        self.isNative = False
        self.name = ""
        self.path = ""
        self.url = ""
        self.isRequire = True
        self.hash = ""


checkOSRules = True
defaultLibraryServer = "https://libraries.minecraft.net/"

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


def nameToPath(name, native):  # library name to relative path
    try:
        tmp = name.split(':')
        front = tmp[0].replace('.', '/')
        back = ""

        for i in range(1, len(tmp)):
            if i == len(tmp) - 1:
                back += tmp[i]
            else:
                back += tmp[i] + ":"

        libpath = front + "/" + back.replace(":", "/") + "/" + (back.replace(":", "-"))
        if native:
            libpath += "-" + native + ".jar"
        else:
            libpath += ".jar"
        return libpath
    except Exception:
        return ""


def checkAllowLibrary(arr):
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

        if not action and containCurrentOS:
            return False
        elif action and containCurrentOS:
            return True
        elif action and not containCurrentOS:
            return False


def createLibrary(name, nativeId, job):
    path = job.get("path")
    if not path:
        path = nameToPath(name, nativeId)

    url = job.get("url")
    if not url:
        url = defaultLibraryServer + path
    elif not url.split('/')[-1]:
        url += path

    library = mlibrary()
    library.hash = job.get("sha1")
    library.name = name
    library.path = os.path.normpath(minecraft.library + "/" + path)
    library.url = url
    if nativeId:
        library.isNative = True
    else:
        library.isNative = False

    return library

def parselist(json):
    list = []

    for item in json:
            name = item.get("name")
            if name is None:
                continue

            # check rules
            rules = item.get("rules")
            if checkOSRules and rules:
                isRequire = checkAllowLibrary(rules)

                if not isRequire:
                    continue

            # forge library
            downloads = item.get("downloads")
            if not downloads:  # downloads == null
                natives = item.get("natives")

                nativeId = None
                if natives is not None:  # natives != null
                    nativeId = natives.get(osname)

                list.append(createLibrary(name, nativeId, item))
                continue

            # native library
            classif = downloads.get("classifiers")
            if classif:
                isgo = True
                nativeId = ""

                if classif.get("natives-windows-64") and osname == "windows" and is64bit:
                    nativeId = "natives-windows-64"
                if classif.get("natives-windows-32") and osname == "windows":
                    nativeId = "natives-windows-32"
                if classif.get("natives-" + osname):
                    nativeId = "natives-" + osname
                else:
                    isgo = False

                job = classif.get(nativeId)
                if isgo:
                    list.append(createLibrary(name, nativeId, job))

            # common library
            arti = downloads.get("artifact")
            if arti:
                list.append(createLibrary(name, "", arti))

    return list

