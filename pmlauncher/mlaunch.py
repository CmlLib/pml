from pmlauncher import mnative, minecraft, mrule
import string
import os
import re

supportversion = "1.4"
pre_compiled = re.compile("\\$\\{(.*?)}")

def e(t):
    if " " in t:
        return '"' + t + '"'
    else:
        return t


def ea(t):
    if " " in t and "=" in t:
        s = t.split("=")
        return s[0] + '="' + s[1] + '"'
    else:
        return t


def arg_in(arg, dicts):
    args = list()
    for item in arg:
        if type(item) is str:
            m = pre_compiled.search(item)  # check ${} str
            if m:
                arg_key = m.group()  # get ${KEY}
                arg_value = dicts.get(arg_key[2:-1])  # get dicts value of ${KEY}

                if arg_value:
                    args.append(pre_compiled.sub(arg_value.replace("\\","\\\\"), item))  # replace ${} of whole str to dicts value
                else:
                    args.append(item)  # if value of default arg has space, handle whitespace.
                                           # (ex) -Dos.Version=Windows 10 => -Dos.Version="Windows 10"
            else:
                args.append(ea(item))  # not ${} str

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
        if mrule.osname == "osx":
            self.defaultJavaParameter += " -XstartOnFirstThread"

        option.checkValid()
        self.launchOption = option

    def createArg(self):
        profile = self.launchOption.start_profile

        args = list()

        # common jvm args
        if self.launchOption.jvm_arg:
            args.append(self.launchOption.jvm_arg)
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
            args.extend(arg_in(profile.jvm_arguments, jvmdict))
        else:
            args.append("-Djava.library.path=" + e(minecraft.natives))
            args.append("-cp " + libs)


        args.append(profile.mainclass)

        # game args
        gamedict = {
            "auth_player_name" : self.launchOption.session.username,
            "version_name" : profile.id,
            "game_directory" : e(minecraft.path),
            "assets_root" : e(minecraft.assets),
            "assets_index_name" : profile.assetId,
            "auth_uuid" : self.launchOption.session.uuid,
            "auth_access_token" : self.launchOption.session.access_token,
            "user_properties" : "{}",
            "user_type" : "Mojang",
            "game_assets" : e(minecraft.assetLegacy),
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

        return " ".join(map(str, args))

    def createProcess(self):
        mnative.clean_natives()
        mnative.extract_natives(self.launchOption.start_profile)

        return self.createArg()


