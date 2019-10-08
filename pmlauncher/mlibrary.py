from pmlauncher import minecraft, mrule
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
                isRequire = mrule.checkAllowOS(rules)

                if not isRequire:
                    continue

            # forge library
            downloads = item.get("downloads")
            if not downloads:  # downloads == null
                natives = item.get("natives")

                nativeId = None
                if natives is not None:  # natives != null
                    nativeId = natives.get(mrule.osname)

                list.append(createLibrary(name, nativeId, item))
                continue

            # native library
            classif = downloads.get("classifiers")
            if classif:
                native_id = None
                native_obj = item.get("natives")
                if native_obj:
                    native_id = native_obj.get(mrule.osname)

                if native_id and classif.get(native_id):
                    native_id = native_id.replace("${arch}", mrule.arch)
                    job = classif.get(native_id)
                    list.append(createLibrary(name, native_id, job))

            # common library
            arti = downloads.get("artifact")
            if arti:
                list.append(createLibrary(name, "", arti))

    return list

