import requests
import json
from pmlauncher import minecraft, mlibrary, mrule
import os


def n(t):
    if t is None:
        return ""
    else:
        return t


def arg_parse(arr):
    strlist = list()
    for item in arr:
        if type(item) == dict:



class profile:
    def __init__(self, info):
        self.id = ""
        self.assetId = ""
        self.assetUrl = ""
        self.assetHash = ""
        self.jvm_arguments = []
        self.game_arguments = []
        self.libraries = []
        self.clientDownloadUrl = ""
        self.clientHash = ""
        self.parent_profile_id = ""
        self.is_inherted = False
        self.jar = ""
        self.mainclass = ""
        self.minecraftArguments = ""
        self.releaseTime = ""
        self.type = ""
        self.parse(info)

    

    def parse(self, info):
        if info.isweb:
            json = requests.get(info.path).text
        else:
            f = open(info.path)
            json = f.read()
            f.close()

        return self.parseFromJson(json)

    def parseFromJson(self, content):
        dict = json.loads(content)

        self.id = dict.get("id")

        assetIndex = dict.get("assetIndex")
        if assetIndex:
            self.assetId = n(assetIndex.get("id"))
            self.assetUrl = n(assetIndex.get("url"))
            self.assetHash = n(assetIndex.get("sha1"))

        downloads = dict.get("downloads")
        if downloads:
            client = downloads.get("client")
            if client:
                self.clientDownloadUrl = client["url"]
                self.clientHash = client["sha1"]

        self.libraries = mlibrary.parselist(dict.get("libraries"))
        self.mainclass = n(dict.get("mainClass"))

        self.minecraftArguments = dict.get("minecraftArguments")
        arg = dict.get("arguments")
        if arg:
            if arg.get("game"):
                self.game_arguments = arg_parse(arg.get("game")
            if arg.get("jvm"):
                self.jvm_arguments = arg_parse(arg.get("jvm")

        self.releaseTime = n(dict.get("releaseTime"))
        self.type = n(dict.get("type"))

        inherits = dict.get("inheritsFrom")
        if inherits:
            self.is_inherited = True
            self.parent_profile_id = inherits
        else:
            self.jar = self.id

        profilePath = os.path.normpath(minecraft.version + "/" + self.id)

        if not os.path.isdir(profilePath):
            os.makedirs(profilePath)

            f = open(os.path.normpath(profilePath + "/" + self.id + ".json"), "w")
            f.write(content)
            f.close()


def get_profile(infos, version):
    for item in infos:
        item.
