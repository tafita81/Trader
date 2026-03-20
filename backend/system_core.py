class SystemCore:
    def __init__(self):
        self.mode = "fund"

    def status(self):
        return {"mode": self.mode}
