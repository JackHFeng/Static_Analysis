from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable


class Variable:
    def __init__(self, variable: Slither_Local_Variable):
        self.name = variable.name
        # print(self.name)
        self.type = variable.type

    def is_state_variable(self):
        return False

    def is_local_variable(self):
        return True

    def __str__(self):
        return self.name + "=>" + self.type

    def __repr__(self):
        return self.name + "=>" + self.type
