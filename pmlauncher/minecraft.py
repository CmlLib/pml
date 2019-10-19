import os

path = ""
library = ""
version = ""
assets = ""
index = ""
assetObject = ""
assetLegacy = ""
resources = ""
natives = ""


def initialize(_path):
    global path, library, version, resources, natives

    path = m(_path)
    library = m(path + "/libraries")
    version = m(path + "/versions")
    resources = m(path + "/resources")
    natives = m(path + "/natives")
    change_assets(path)


def change_assets(p):
    global assets, assetLegacy, assetObject, index

    assets = os.path.normpath(p + "/assets")
    index = os.path.normpath(assets + "/indexes")
    assetObject = os.path.normpath(assets + "/objects")
    assetLegacy = os.path.normpath(assets + "/virtual/legacy")


def m(p):
    p = os.path.normpath(p)
    if not os.path.isdir(p):
        os.makedirs(p)
    return p

