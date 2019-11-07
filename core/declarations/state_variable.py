from .variable import Variable
from slither.core.variables.state_variable import StateVariable as Slither_State_Variable


class StateVariable(Variable):
    def __init__(self, variable: Slither_State_Variable):
        self.name = variable.name
        self.type = variable.type
        self.visibility = variable.visibility
        # self.initialized = variable.initialized
        # print(type(variable.initialized))   # May need to investigate what these are
        self.functions_read = set()
        self.functions_written = set()
        # self.f_write_conditions = []
        self.modifiers_read = set()
        self.modifiers_written = set()

        self.requires_read = set()

    def is_state_variable(self):
        return True

    def is_local_variable(self):
        return False
