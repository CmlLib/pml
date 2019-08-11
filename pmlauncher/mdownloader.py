import os
import requests
from pmlauncher import minecraft, mevent
import json
from shutil import copyfile
import hashlib


def mkd(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def download(url, path):
    dirpath = os.path.dirname(path)
    mkd(dirpath)

    response = requests.get(url)
    if int(response.status_code / 100) is not 2:
        return

    f = open(path, "wb")
    f.write(response.content)
    f.close()


class mdownload:
    def __init__(self, _profile):
        self.checkHash = True
        self.profile = _profile
        self.doFireEvents = True
        self.downloadFileChangedEvent = mevent.Event()

    def fireEvent(self, kind, name, max, current):
        if not self.doFireEvents:
            return

        args = mevent.MDownloadEventArgs()
        args.filekind = kind
        args.filename = name
        args.maxvalue = max
        args.currentvalue = current
        self.downloadFileChangedEvent(args)

    def checkFileSHA1(self, path, fhash):
        if not self.checkHash:
            return True
        if not fhash:
            return True

        f = open(path, "rb")
        data = f.read()
        f.close()

        return fhash == hashlib.sha1(data).hexdigest()

    def checkFileValidation(self, path, fhash):
        return os.path.isfile(path) and self.checkFileSHA1(path, fhash)

    def downloadAll(self, downloadAssets):
        self.downloadLibraries()
        self.downloadMinecraft()
        if downloadAssets:
            self.downloadIndex()
            self.downloadResources()

    def downloadLibraries(self):
        count = len(self.profile.libraries)
        for i in range(0, count):
            lib = self.profile.libraries[i]
            if lib.isRequire and lib.path and lib.url and not self.checkFileValidation(lib.path, lib.hash):
                download(lib.url, lib.path)

            self.fireEvent("library", lib.name, count, i + 1)

    def downloadIndex(self):
        path = os.path.normpath(minecraft.index + "/" + self.profile.assetId + ".json")
        if self.profile.assetUrl and not self.checkFileValidation(path, self.profile.assetHash):
            download(self.profile.assetUrl, path)

        self.fireEvent("index", self.profile.assetId, 1, 1)

    def downloadResources(self):
        indexPath = os.path.normpath(minecraft.index + "/" + self.profile.assetId + ".json")
        if not os.path.isfile(indexPath):
            return

        f = open(indexPath, "r")
        content = f.read()
        f.close()

        index = json.loads(content)

        isVirtual = False
        v = index.get("virtual")
        if v and v == "true":
            isVirtual = True

        items = list(index.get("objects").items())
        count = len(items)
        for i in range(0, count):
            key = items[i][0]
            value = items[i][1]

            hash = value.get("hash")
            hashName = hash[:2] + "/" + hash
            hashPath = os.path.normpath(minecraft.assetObject + "/" + hashName)
            hashUrl = "http://resources.download.minecraft.net/" + hashName

            if not os.path.isfile(hashPath):
                download(hashUrl, hashPath)

            if isVirtual:
                resPath = os.path.normpath(minecraft.assetLegacy + "/" + key)

                if not os.path.isfile(resPath):
                    mkd(os.path.dirname(resPath))
                    copyfile(hashPath, resPath)

            self.fireEvent("resource", "", count, i + 1)

    def downloadMinecraft(self):
        if not self.profile.clientDownloadUrl:
            return

        id = self.profile.id
        path = os.path.normpath(minecraft.version + "/" + id + "/" + id + ".jar")
        if not self.checkFileValidation(path, self.profile.clientHash):
            download(self.profile.clientDownloadUrl, path)

        self.fireEvent("minecraft", id, 1, 1)
