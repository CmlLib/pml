import os
from launcher import minecraft
import json
import requests


class mprofileinfo:
    def __init__(self):
        self.isweb = True
        self.name = ""
        self.path = ""


def getProfilesFromLocal():
    files = os.listdir(minecraft.version)
    arr = list()

    if not files:
        return arr

    for item in files:
        filepath = os.path.normpath(minecraft.version + "/" + item + "/" + item + ".json")
        if os.path.isfile(filepath):
            profile = mprofileinfo()
            profile.isweb = False
            profile.name = item
            profile.path = filepath
            arr.append(profile)

    return arr


def getProfilesFromWeb():
    result = list()
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    jarr = json.loads(requests.get(url).text)
    for item in jarr.get("versions"):
        profile = mprofileinfo()
        profile.isweb = True
        profile.name = item.get("id")
        profile.path = item.get("url")
        result.append(profile)

    return result


def getProfiles():
    arr = getProfilesFromLocal()
    for item1 in getProfilesFromWeb():
        exist = False
        for item2 in arr:
            if item1.name == item2.name:
                exist = True
                break
        if not exist:
            arr.append(item1)
    return arr