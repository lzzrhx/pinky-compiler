class Environment:
    def __init__(self, parent = None):
        self.vars = {} # Dictionary to store variable names / values
        self.parent = parent

    def get_var(self, name):
        env = self
        while env.vars.get(name) is None and env.parent is not None:
            env = env.parent
        return env.vars.get(name)

    def set_var(self, name, value):
        env = self
        while env.vars.get(name) is None and env.parent is not None:
            env = env.parent
        if env.vars.get(name) is None:
            env = self
        env.vars[name] = value

    def new_env(self):
        '''
        Return a new environment that is a child of the current one
        Used to create a new nested scope (while, funcs, etc.)
        '''
        return Environment(parent=self)

