class launchoption:
    def __init__(self):
        self.maximumRamSizeMB = 1024
        self.startProfile = None
        self.baseProfile = None
        self.session = None
        self.launcherName = ""
        self.serverIp = ""
        self.customJavaParameter = ""
        self.screenWidth = 0
        self.screenHeight = 0

    def checkValid(self):
        exMsg = ""
        if not self.maximumRamSizeMB:
            exMsg = "maximumRamSize is too small"
        if not self.startProfile:
            exMsg = "startProfile was None"
        if not self.session:
            exMsg = "session was None"
        if " " in self.launcherName:
            exMsg = "launcherName cannot contain space character"

        if exMsg:
            raise ValueError(exMsg)
