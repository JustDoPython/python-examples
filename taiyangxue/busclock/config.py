class Config:
    def __init__(self, config):
        self.loopWaitSeconds = config.get("loopWaitSeconds", 60)
        self.spurtWaitSeconds = config.get("spurtWaitSeconds", 10)
        self.mailConfig = config.get("mailConfig", None)
        self.latestLeaveMinute = config.get("latestLeaveTime", 5)
        self.lines = config.get("lines", {})