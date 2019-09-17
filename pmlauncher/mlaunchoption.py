class launchoption:
    def __init__(self):
        self.xmx_mb = 1024
        self.start_profile = None
        self.session = None
        self.launcher_name = ""
        self.server_ip = ""
        self.jvm_arg = ""
        self.screen_width = 0
        self.screen_height = 0

    def checkValid(self):
        exMsg = ""
        if not self.xmx_mb:
            exMsg = "xmx_mb is too small"
        if not self.start_profile:
            exMsg = "start_profile was None"
        if not self.session:
            exMsg = "session was None"
        if " " in self.launcher_name:
            exMsg = "launcher_name cannot contain space character"

        if exMsg:
            raise ValueError(exMsg)

