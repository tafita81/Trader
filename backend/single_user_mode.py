# Single User Mode (modo pessoal - sem SaaS)
# - força uso local
# - desativa multi-user
# - conecta tudo para um único operador

class SingleUserConfig:

    def __init__(self):
        self.mode = "single_user"
        self.user = "owner"
        self.capital = 100
        self.risk = 0.03

        # módulos ativos
        self.modules = {
            "global_allocator": True,
            "regime_ai": True,
            "genetic": True,
            "multi_agent": True,
            "deep_rl": True,
            "market_making": True,
            "execution": True,
            "auto_optimizer": True,
            "scenario_engine": True
        }


class SingleUserManager:

    def __init__(self, config: SingleUserConfig):
        self.config = config

    def get_user(self):
        return self.config.user

    def get_capital(self):
        return self.config.capital

    def update_capital(self, new_capital):
        self.config.capital = new_capital

    def get_risk(self):
        return self.config.risk

    def update_risk(self, risk):
        self.config.risk = risk

    def is_enabled(self, module):
        return self.config.modules.get(module, False)


# ===== USO =====
# config = SingleUserConfig()
# manager = SingleUserManager(config)
