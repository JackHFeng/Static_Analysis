class Contract:
    def __init__(self):
        self.name = ''

        self.functions = {}
        self.state_variables = {}
        self.modifiers = {}

    def get_functions(self):
        return self.functions.values()

    def get_state_variables(self):
        return self.state_variables.values()

    def get_modifiers(self):
        return self.modifiers.values()