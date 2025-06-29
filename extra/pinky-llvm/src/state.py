class Environment:
    def __init__(self, parent = None):
        self.vars = {} # Dictionary to store variable names / values
        self.funcs = {} # Dictionary to store functions
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

    def set_local(self, name, value):
        '''
        Sets a new variable in the current environment (shadowing any previous values of that variable name)
        '''
        self.vars[name] = value

    def get_func(self, name):
        '''
        Searches the current environment and all parent environments for a function name
        '''
        while self:
            value = self.funcs.get(name)
            if value is not None:
                return value
            else:
                self = self.parent
        return None

    def set_func(self, name, value):
        '''
        Declares a function (also stores the environment / context in which it was declared)
        '''
        self.funcs[name] = value

    def new_env(self):
        '''
        Return a new environment that is a child of the current one
        Used to create a new nested scope (while, funcs, etc.)
        '''
        return Environment(parent=self)

