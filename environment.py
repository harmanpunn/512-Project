"""

Singleton class to hold all the environment constants

"""
class Environment:
    instances = []

    def __init__(self, ui,nc) -> None:
        if len(Environment.instances)==0:
            self.ui = ui
            self.node_count = nc
            Environment.instances.append(self)
        else:
            raise RuntimeError("Initialising Environment multiple times!")
    
    @classmethod
    def getInstance(cls):
        if len(Environment.instances)==0:
            raise RuntimeError("Environment not initialised!")
        return Environment.instances[0]