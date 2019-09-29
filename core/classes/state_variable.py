from .variable import Variable


class StateVariable(Variable):
    def __init__(self):
        super().__init__()
        self.visibility = ''
        self.initialized = False

        self.functions_read = []
        self.functions_written = []
        # self.f_write_conditions = []
        self.modifiers_read = []
        self.modifiers_written = []

        self.requires = []

    def is_state_variable(self):
        return True

    def requires_appeared_in(self):
        return self.requires

    def functions_read(self):
        return self.functions_read

    def functions_written(self):
        return self.functions_written

    def modifiers_read(self):
        return self.modifiers_read

    def modifiers_written(self):
        return self.modifiers_written
