from pmlauncher import minecraft
import zipfile
import os


def extract_natives(profile):
    for item in profile.libraries:
        if item.isNative:
            try:
                lib = zipfile.ZipFile(item.path)
                lib.extractall(minecraft.natives)
            except Exception as e:
                print(e)


def clean_natives():
    for item in os.listdir(minecraft.natives):
       path = os.path.join(minecraft.natives, item)
       
       if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                print(e)

