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
    global path, library, version, assets, index, assetObject, assetLegacy, resources, natives

    path = os.path.normpath(_path)
    library = os.path.normpath(path + "/libraries")
    version = os.path.normpath(path + "/versions")
    assets = os.path.normpath(path + "/assets")
    index = os.path.normpath(assets + "/indexes")
    assetObject = os.path.normpath(assets + "/objects")
    assetLegacy = os.path.normpath(assets + "/virtual/legacy")
    resources = os.path.normpath(path + "/resources")
    natives = os.path.normpath(path + "/natives")

    mkd(path)
    mkd(library)
    mkd(version)
    mkd(index)
    mkd(assetLegacy)
    mkd(assetObject)
    mkd(resources)
    mkd(natives)


def mkd(p):
    if not os.path.isdir(p):
        os.makedirs(p)
