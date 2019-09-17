from pmlauncher import minecraft
import zipfile
import os


class native:
    def __init__(self, _launchOption):
        self.launchOption = _launchOption

    def extractNatives(self, profile):
        for item in profile.libraries:
            if item.isNative:
                try:
                    lib = zipfile.ZipFile(item.path)
                    lib.extractall(minecraft.natives)
                except Exception:
                    pass

    def createNatives(self):
        self.extractNatives(self.launchOption.start_profile)

    def cleanNatives(self):
        for item in os.listdir(minecraft.natives):
            if os.path.isfile(item):
                try:
                    os.remove(item)
                except Exception:
                    pass

