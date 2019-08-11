import requests
import json
from pmlauncher import minecraft, mlibrary
import os


def n(t):
    if t is None:
        return ""
    else:
        return t


class profile:
    def __init__(self, info):
        self.id = ""
        self.assetId = ""
        self.assetUrl = ""
        self.assetHash = ""
        self.arguments = []
        self.libraries = []
        self.clientDownloadUrl = ""
        self.clientHash = ""
        self.innerJarId = ""
        self.isForge = False
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
        self.arguments = dict.get("arguments")

        self.releaseTime = n(dict.get("releaseTime"))
        self.type = n(dict.get("type"))

        jar = dict.get("jar")
        if jar:
            self.isForge = True
            self.innerJarId = jar
        else:
            self.isForge = False

        profilePath = os.path.normpath(minecraft.version + "/" + self.id)

        if not os.path.isdir(profilePath):
            os.makedirs(profilePath)

            f = open(os.path.normpath(profilePath + "/" + self.id + ".json"), "w")
            f.write(content)
            f.close()