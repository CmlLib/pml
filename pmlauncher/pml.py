from . import *

profiles = None
downloadEventHandler = None


def getGamePath():
    return minecraft.path


def initialize(path):
    minecraft.initialize(path)


def updateProfiles():
    global profiles
    profiles = mprofileinfo.getProfiles()
    return profiles


def getProfile(name):
    global profiles
    if profiles is None:
        updateProfiles()

    return mprofile.get_profile(profiles, name)


def downloadProfile(profile, downloadAssets = True):
    if type(profile) is not mprofile.profile:
        raise ValueError("profile must be mprofile.profile type")

    downloader = mdownloader.mdownload(profile)
    if downloadEventHandler:
        downloader.downloadFileChangedEvent.append(downloadEventHandler)
    downloader.downloadAll(downloadAssets)


def startProfile(name, **option):
    profile = getProfile(name)
    downloadProfile(profile)

    l = mlaunchoption.launchoption()
    if option.get("launchoption"):
        l = option.get("launchoption")
    else:
        l.__dict__.update(option)
    
    l.start_profile = profile
    launch = mlaunch.launch(l)
    return launch.createProcess()
