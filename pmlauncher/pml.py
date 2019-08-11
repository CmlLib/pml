from pmlauncher import minecraft, mlaunch, mdownloader, mprofile, mlaunchoption, mprofileinfo

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

    for item in profiles:
        if item.name == name:
            return mprofile.profile(item)

    raise ValueError("can't find profile named " + name)


def downloadProfile(profile, downloadAssets):
    if type(profile) is not mprofile.profile:
        raise ValueError("profile must be mprofile.profile type")

    downloader = mdownloader.mdownload(profile)
    downloader.downloadFileChangedEvent.append(downloadEventHandler)
    downloader.downloadAll(downloadAssets)


def startProfile(name, option):
    if type(option) is not mlaunchoption.launchoption:
        raise ValueError("option must be mlaunchoption.launchoption type")

    profile = getProfile(name)
    baseProfile = None

    if profile.isForge:
        baseProfile = getProfile(profile.innerJarId)
        downloadProfile(baseProfile, True)

    downloadProfile(profile, not profile.isForge)  # if profile is forge, do not download assets

    option.startProfile = profile
    option.baseProfile = baseProfile
    launch = mlaunch.launch(option)
    return launch.createProcess()
