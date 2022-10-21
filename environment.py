"""

Singleton class to hold all the environment constants

"""
class Environment:
    
    # to keep track of instances
    instances = []

    # initializes the environment
    # Throws RuntimeError if called more than once
    def __init__(self, ui,nc) -> None:
        if len(Environment.instances)==0:
            self.ui = ui
            self.node_count = nc
            Environment.instances.append(self)
        else:
            raise RuntimeError("Initialising Environment multiple times!")
    
    # to get the instance of the environment class
    @classmethod
    def getInstance(cls):
        if len(Environment.instances)==0:
            raise RuntimeError("Environment not initialised!")
        return Environment.instances[0]