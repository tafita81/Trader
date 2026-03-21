class FundMode:
    def __init__(self):
        self.enabled = True

    def status(self):
        return {"fund_mode": self.enabled}
