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
            allow = True

            rule = item.get("rules")            
            if rule:
                allow = mrule.checkAllowOS(rule)

            value = item.get("value")

            if allow and value:
                if type(value) == list:
                    strlist.extend(value)
                else:
                    strlist.append(value)
        else:
            strlist.append(item)

    return strlist



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
        self.is_inherited = False
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
        d = json.loads(content)

        self.id = d.get("id")

        assetIndex = d.get("assetIndex")
        if assetIndex:
            self.assetId = n(assetIndex.get("id"))
            self.assetUrl = n(assetIndex.get("url"))
            self.assetHash = n(assetIndex.get("sha1"))

        downloads = d.get("downloads")
        if downloads:
            client = downloads.get("client")
            if client:
                self.clientDownloadUrl = client["url"]
                self.clientHash = client["sha1"]

        self.libraries = mlibrary.parselist(d.get("libraries"))
        self.mainclass = n(d.get("mainClass"))

        self.minecraftArguments = d.get("minecraftArguments")
        arg = d.get("arguments")
        if arg:
            if arg.get("game"):
                self.game_arguments = arg_parse(arg.get("game"))
            if arg.get("jvm"):
                self.jvm_arguments = arg_parse(arg.get("jvm"))

        self.releaseTime = n(d.get("releaseTime"))
        self.type = n(d.get("type"))

        inherits = d.get("inheritsFrom")
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


def inhert(parent, child):
    # Overload : assetId, assetUrl, assetHash, clientDownloadUrl, clientHash, mainClass, minecraftArguments
    # Combine : libraries, game_arguments, jvm_arguments

    if not child.assetId:
        child.assetId = parent.assetId

    if not child.assetUrl:
        child.assetUrl = parent.assetUrl

    if not child.assetHash:
        child.assetHash = parent.assetHash

    if not child.clientDownloadUrl:
        child.clientDownloadUrl = parent.clientDownloadUrl

    if not child.clientHash:
        child.clientHash = parent.clientHash

    if not child.mainclass:
        child.mainclass = parent.mainclass

    if not child.minecraftArguments:
        child.minecraftArguments = parent.minecraftArguments

    if parent.libraries:
        if child.libraries:
            child.libraries.extend(parent.libraries)
        else:
            child.libraries = parent.libraries

    if parent.game_arguments:
        if child.game_arguments:
            child.game_arguments.extend(parent.game_arguments)
        else:
            child.game_arguments = parent.game_arguments

    if parent.jvm_arguments:
        if child.jvm_arguments:
            child.jvm_arguments.extend(parent.jvm_arguments)
        else:
            child.jvm_arguments = parent.jvm_arguments


def get_profile(infos, version):
    start_profile = None

    for item in infos:
        if item.name == version:
            start_profile = profile(item)
            break
    
    if start_profile == None:
        raise ValueError("cannot find profile named " + version)

    if start_profile.is_inherited:
        parent_profile = get_profile(infos, start_profile.parent_profile_id)
        inhert(parent_profile, start_profile)

    return start_profile
