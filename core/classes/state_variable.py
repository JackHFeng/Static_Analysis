from .variable import Variable

class State_Variable(Variable):
    def __init__(self):
        super().__init__()
        self.visibility = ''
        self.initialized = False

        self.f_read = []
        self.f_written = []
        # self.f_write_conditions = []

        self.requires = []

    def is_stateVariable(self):
        return True

    def requires_appeared_in(self):
        return self.requires

    def functions_read(self):
        return self.f_read

    def functions_written(self):
        return self.f_written