from pmlauncher import mnative, minecraft
import string
import os

supportversion = "1.4"

def e(t):
    if " " in t:
        return '"' + t + '"'
    else:
        return t


def arg_in(arg, dicts):
    args = list()
    for item in arg:
        if type(item) is str:
            if item[0] is not "$":
                args.append(item)
            else:
                argValue = dicts.get(item[2:-1])  # remove ${  }
                if argValue:
                    args.append(e(argValue))
                else:
                    args.append(item)
    return args


def arg_str(arg, dicts):
    return string.Template(arg).safe_substitute(dicts)


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
        profile = self.launchOption.start_profile

        args = list()

        # common jvm args
        if self.launchOption.jvm_args:
            args.append(self.launchOption.jvm_args)
        else:
            args.append(self.defaultJavaParameter)

        args.append("-Xmx" + str(self.launchOption.xmx_mb) + "m")

        # specific jvm args
        libArgs = list()

        for item in profile.libraries:
            if not item.isNative:
                libArgs.append(e(item.path))

        libArgs.append(e(os.path.normpath(minecraft.version + "/" + profile.jar + "/" + profile.jar + ".jar")))
        libs = os.pathsep.join(libArgs)

        jvmdict = {
            "natives_directory" : e(minecraft.natives),
            "launcher_name" : "minecraft-launcher",
            "launcher_version" : "2",
            "classpath" : libs
        }

        if profile.jvm_arguments:
            args.append(arg_str(" ".join(profile.jvm_arguments), jvmdict))           
        else:
            args.extend[
                "-Djava.library.path=",
                e(minecraft.natives),
                "-cp",
                libs]


        args.append(profile.mainclass)

        # game args
        gamedict = {
            "auth_player_name" : self.launchOption.session.username,
            "version_name" : profile.id,
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

        if self.launchOption.launcher_name:
            gamedict["version_type"] = self.launchOption.launcher_name
        else:
            gamedict["version_type"] = profile.type

        if profile.game_arguments:  # 1.3
            args.extend(arg_in(profile.game_arguments, gamedict))
        elif profile.minecraftArguments:
            args.append(arg_str(profile.minecraftArguments, gamedict))

        # options
        if self.launchOption.server_ip:
            args.append("--server " + self.launchOption.server_ip)

        if self.launchOption.screen_width and self.launchOption.screen_height:
            args.append("--width " + self.launchOption.screen_width)
            args.append("--height ", self.launchOption.screen_height)

        return " ".join(args)

    def createProcess(self):
        mnative.clean_natives()
        mnative.extract_natives(self.launchOption.start_profile)

        return self.createArg()
