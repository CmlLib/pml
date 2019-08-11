from launcher import mnative, minecraft
import string
import os

supportversion = "1.4"

def e(t):
    if " " in t:
        return '"' + t + '"'
    else:
        return t

class launch:
    def __init__(self, option):
        self.defaultJavaParameter = " ".join([
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:+UseG1GC",
            "-XX:G1NewSizePercent=20",
            "-XX:G1ReservePercent=20",
            "-XX:MaxGCPauseMillis=50",
            "-XX:G1HeapRegionSize=16M"])

        option.checkValid()
        self.launchOption = option

    def createArg(self):
        profile = self.launchOption.startProfile
        hasBase = self.launchOption.baseProfile is not None
        if hasBase:
            profile = self.launchOption.baseProfile

        args = list()

        # java args
        if self.launchOption.customJavaParameter:
            args.append(self.launchOption.customJavaParameter)
        else:
            args.append(self.defaultJavaParameter)

        args.append("-Xmx" + str(self.launchOption.maximumRamSizeMB) + "m")
        args.append("-Djava.library.path=" + e(minecraft.natives))
        args.append("-cp")

        libArgs = list()

        if hasBase:  # forge library
            for item in self.launchOption.startProfile.libraries:
                if not item.isNative:
                    libArgs.append(e(item.path))

        for item in profile.libraries:  # common library
            if not item.isNative:
                libArgs.append(e(item.path))

        libArgs.append(e(os.path.normpath(minecraft.version + "/" + profile.id + "/" + profile.id + ".jar")))
        args.append(os.pathsep.join(libArgs))
        args.append(self.launchOption.startProfile.mainclass)

        # game args
        argDict = {
            "auth_player_name" : self.launchOption.session.username,
            "version_name" : self.launchOption.startProfile.id,
            "game_directory" : minecraft.path,
            "assets_root" : minecraft.assets,
            "assets_index_name" : profile.assetId,
            "auth_uuid" : self.launchOption.session.uuid,
            "auth_access_token" : self.launchOption.session.access_token,
            "user_properties" : "{}",
            "user_type" : "Mojang",
            "game_assets" : minecraft.assetLegacy,
            "auth_session" : self.launchOption.session.access_token
        }

        if self.launchOption.launcherName:
            argDict["version_type"] = self.launchOption.launcherName
        else:
            argDict["version_type"] = profile.type

        if self.launchOption.startProfile.arguments:  # 1.3
            for item in self.launchOption.startProfile.arguments.get("game"):
                if type(item) is str:
                    if item[0] is not "$":
                        args.append(item)
                    else:
                        argValue = argDict.get(item[2:-1])  # remove ${  }
                        if argValue:
                            args.append(e(argValue))
                        else:
                            args.append(item)
        else:
            gameArgs = string.Template(self.launchOption.startProfile.minecraftArguments).safe_substitute(argDict)
            args.append(gameArgs)

        # options
        if self.launchOption.serverIp:
            args.append("--server " + self.launchOption.serverIp)

        if self.launchOption.screenWidth and self.launchOption.screenHeight:
            args.append("--width " + self.launchOption.screenWidth)
            args.append("--height ", self.launchOption.screenHeight)

        return " ".join(args)

    def createProcess(self):
        native = mnative.native(self.launchOption)
        native.cleanNatives()
        native.createNatives()

        return self.createArg()
